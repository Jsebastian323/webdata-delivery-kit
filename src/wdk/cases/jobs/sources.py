"""Adapters for public job-board APIs. Each one turns a board into raw posting dicts with the
same shape, so everything downstream (enrichment, families, diffing) is source-agnostic.

All three endpoints are the public ones the boards expose for embedding job listings:

* Workable:   GET https://apply.workable.com/api/v1/widget/accounts/{board}?details=true
* Greenhouse: GET https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true
* Lever:      GET https://api.lever.co/v0/postings/{board}?mode=json

One request per board returns every posting with its description.
"""

from __future__ import annotations

import datetime as dt
import html
import re
from dataclasses import dataclass

from ...fetch import Fetcher
from ...normalize import clean_text, fold, html_to_text

# Country names (English and Spanish) and a few big cities, folded, mapped to ISO 3166-1 alpha-2.
_PLACES = {
    "colombia": "CO", "bogota": "CO", "medellin": "CO", "barranquilla": "CO", "cali": "CO",
    "mexico": "MX", "mexico city": "MX", "ciudad de mexico": "MX", "guadalajara": "MX",
    "brazil": "BR", "brasil": "BR", "sao paulo": "BR", "argentina": "AR", "buenos aires": "AR",
    "chile": "CL", "peru": "PE", "lima": "PE", "uruguay": "UY", "ecuador": "EC", "costa rica": "CR",
    "jamaica": "JM", "venezuela": "VE", "bolivia": "BO", "paraguay": "PY", "panama": "PA",
    "guatemala": "GT", "dominican republic": "DO", "puerto rico": "PR",
    "united states": "US", "usa": "US", "u.s.": "US", "us": "US", "san francisco": "US",
    "new york": "US", "seattle": "US", "austin": "US", "boston": "US", "los angeles": "US",
    "chicago": "US", "washington": "US", "denver": "US", "atlanta": "US", "miami": "US",
    "st. louis": "US", "florida": "US", "texas": "US", "california": "US",
    "canada": "CA", "toronto": "CA", "vancouver": "CA", "montreal": "CA",
    "united kingdom": "GB", "uk": "GB", "england": "GB", "london": "GB", "ireland": "IE", "dublin": "IE",
    "germany": "DE", "berlin": "DE", "france": "FR", "paris": "FR", "spain": "ES", "madrid": "ES",
    "portugal": "PT", "italy": "IT", "netherlands": "NL", "amsterdam": "NL", "belgium": "BE",
    "switzerland": "CH", "austria": "AT", "sweden": "SE", "norway": "NO", "denmark": "DK",
    "finland": "FI", "iceland": "IS", "poland": "PL", "warsaw": "PL", "romania": "RO",
    "bulgaria": "BG", "hungary": "HU", "czechia": "CZ", "czech republic": "CZ", "slovakia": "SK",
    "greece": "GR", "serbia": "RS", "cyprus": "CY", "malta": "MT", "lithuania": "LT", "latvia": "LV",
    "turkey": "TR", "israel": "IL", "united arab emirates": "AE", "uae": "AE", "saudi arabia": "SA",
    "qatar": "QA", "egypt": "EG", "morocco": "MA", "kenya": "KE", "nigeria": "NG",
    "south africa": "ZA", "india": "IN", "bengaluru": "IN", "bangalore": "IN", "hyderabad": "IN",
    "philippines": "PH", "manila": "PH", "malaysia": "MY", "indonesia": "ID", "singapore": "SG",
    "japan": "JP", "tokyo": "JP", "south korea": "KR", "australia": "AU", "sydney": "AU",
    "new zealand": "NZ", "pakistan": "PK", "vietnam": "VN", "china": "CN",
}
_PLACE_PATTERN = re.compile(
    r"(?<![a-z])(" + "|".join(re.escape(p) for p in sorted(_PLACES, key=len, reverse=True)) + r")(?![a-z])"
)
LATAM_WORDS = ("latam", "latin america", "south america", "americas")
ANYWHERE_WORDS = ("worldwide", "anywhere", "global", "international")


def countries_in(text: str) -> set[str]:
    """ISO codes of the countries and big cities named in a location string."""
    return {_PLACES[m] for m in _PLACE_PATTERN.findall(fold(text))}


def open_to_colombia(
    countries: set[str] | tuple[str, ...], location: str, remote: bool | None
) -> bool | None:
    """True if Colombia or a LatAm/worldwide remote scope is named; False if the posting names
    only other countries; None when the posting does not say (e.g. just "Remote")."""
    folded = fold(location)
    if "CO" in countries or any(w in folded for w in LATAM_WORDS):
        return True
    if remote and any(w in folded for w in ANYWHERE_WORDS):
        return True
    return False if countries else None


def _date(value) -> dt.date | None:
    if not value:
        return None
    if isinstance(value, (int, float)):  # Lever: epoch milliseconds
        return dt.datetime.fromtimestamp(value / 1000, dt.UTC).date()
    return dt.date.fromisoformat(str(value)[:10])


@dataclass(frozen=True)
class Board:
    company: str
    source: str
    board: str


def _raw(board: Board, **fields) -> dict:
    countries = set(fields.pop("countries"))
    location = clean_text(fields.pop("location"))
    countries |= countries_in(location)
    remote = fields.pop("remote")
    return {
        "key": f"{board.source}:{board.board}:{fields['posting_id']}",
        "source": board.source,
        "company": board.company,
        "location": location,
        "countries": sorted(countries),
        "remote": remote,
        "open_to_colombia": open_to_colombia(countries, location, remote),
        **fields,
    }


def workable_postings(board: Board, payload: dict) -> list[dict]:
    """The widget API repeats a posting once per location (448 entries for 92 postings on the
    first run; the unique-key gate caught it). Entries are merged by shortcode."""
    merged: dict[str, dict] = {}
    for job in payload.get("jobs", []):
        places = [{"country": job.get("country"), "countryCode": None, "city": job.get("city")}]
        places += job.get("locations") or []
        entry = merged.setdefault(job["shortcode"], {"job": job, "places": []})
        entry["places"] += places
    postings = []
    for shortcode, entry in merged.items():
        job, places = entry["job"], entry["places"]
        names = dict.fromkeys(", ".join(p for p in (pl.get("city"), pl.get("country")) if p) for pl in places)
        postings.append(_raw(
            board,
            posting_id=shortcode,
            title=clean_text(job["title"]),
            url=job["url"],
            location="; ".join(n for n in names if n),
            countries={(pl.get("countryCode") or "").upper() for pl in places if pl.get("countryCode")},
            remote=bool(job.get("telecommuting")),
            employment_type=job.get("employment_type") or None,
            published=_date(job.get("published_on")),
            description=html_to_text(job.get("description") or ""),
        ))
    return postings


def greenhouse_postings(board: Board, payload: dict) -> list[dict]:
    postings = []
    for job in payload.get("jobs", []):
        location = (job.get("location") or {}).get("name") or ""
        postings.append(_raw(
            board,
            posting_id=str(job["id"]),
            title=clean_text(job["title"]),
            url=job["absolute_url"],
            location=location,
            countries=set(),
            remote=True if "remote" in location.lower() else None,
            employment_type=None,
            published=_date(job.get("first_published") or job.get("updated_at")),
            description=html_to_text(html.unescape(job.get("content") or "")),
        ))
    return postings


def lever_postings(board: Board, payload: list) -> list[dict]:
    postings = []
    for job in payload:
        categories = job.get("categories") or {}
        places = [categories.get("location") or ""] + list(categories.get("allLocations") or [])
        sections = [job.get("descriptionPlain") or ""]
        for block in job.get("lists") or []:
            sections.append(clean_text(block.get("text")))
            sections.append(html_to_text(block.get("content") or ""))
        sections.append(job.get("additionalPlain") or "")
        workplace = (job.get("workplaceType") or "").lower()
        postings.append(_raw(
            board,
            posting_id=job["id"],
            title=clean_text(job["text"]),
            url=job["hostedUrl"],
            location="; ".join(dict.fromkeys(p for p in places if p)),
            countries={job["country"].upper()} if job.get("country") else set(),
            remote=True if workplace == "remote" else (False if workplace in ("on-site", "onsite") else None),
            employment_type=categories.get("commitment"),
            published=_date(job.get("createdAt")),
            description="\n".join(s for s in sections if s),
        ))
    return postings


ENDPOINTS = {
    "workable": ("https://apply.workable.com/api/v1/widget/accounts/{board}", {"details": "true"},
                 workable_postings),
    "greenhouse": ("https://boards-api.greenhouse.io/v1/boards/{board}/jobs", {"content": "true"},
                   greenhouse_postings),
    "lever": ("https://api.lever.co/v0/postings/{board}", {"mode": "json"}, lever_postings),
}


async def fetch_board(fetcher: Fetcher, board: Board) -> list[dict]:
    url, params, normalize = ENDPOINTS[board.source]
    return normalize(board, await fetcher.get_json(url.format(board=board.board), params=params))
