import re

from wdk.sheets import cell_value, column_letter, upsert_rows


class FakeWorksheet:
    """The four gspread Worksheet methods the upsert uses, backed by a list of rows."""

    def __init__(self, values=None):
        self.values = [list(r) for r in values or []]

    def get_all_values(self):
        return [list(r) for r in self.values]

    def update(self, values, range_name):
        assert range_name == "A1"
        if self.values:
            self.values[0] = list(values[0])
        else:
            self.values.append(list(values[0]))

    def batch_update(self, data):
        for item in data:
            row = int(re.search(r"\d+", item["range"]).group())
            self.values[row - 1] = list(item["values"][0])

    def append_rows(self, rows, value_input_option=None):
        self.values.extend(list(r) for r in rows)


ROWS = [{"id": "1", "title": "Data Engineer", "pay": 25}, {"id": "2", "title": "Designer", "pay": None}]


def test_empty_sheet_gets_header_and_rows():
    ws = FakeWorksheet()
    result = upsert_rows(ws, ROWS, key="id")
    assert ws.values == [["id", "title", "pay"], ["1", "Data Engineer", "25"], ["2", "Designer", ""]]
    assert (result.inserted, result.updated) == (2, 0)


def test_rerun_is_idempotent():
    ws = FakeWorksheet()
    upsert_rows(ws, ROWS, key="id")
    result = upsert_rows(ws, ROWS, key="id")
    assert len(ws.values) == 3
    assert (result.inserted, result.updated, result.unchanged) == (0, 0, 2)


def test_columns_are_found_by_header_name_and_manual_edits_survive():
    ws = FakeWorksheet([
        ["title", "owner", "id", "pay"],          # reordered, plus a column people added by hand
        ["Data Engineer", "Ana", "1", "20"],
        ["Designer", "Luis", "2", "31"],
    ])
    result = upsert_rows(ws, ROWS, key="id")
    assert ws.values[1] == ["Data Engineer", "Ana", "1", "25"]  # updated in place
    assert ws.values[2] == ["Designer", "Luis", "2", "31"]      # empty pay did not erase 31
    assert (result.updated, result.unchanged) == (1, 1)


def test_new_columns_are_added_at_the_end():
    ws = FakeWorksheet([["id", "title"], ["1", "Data Engineer"]])
    upsert_rows(ws, [{"id": "1", "title": "Data Engineer", "countries": ["CO", "MX"]}], key="id")
    assert ws.values == [["id", "title", "countries"], ["1", "Data Engineer", "CO|MX"]]


def test_helpers():
    assert [column_letter(i) for i in (0, 25, 26, 51)] == ["A", "Z", "AA", "AZ"]
    assert cell_value(True) == "TRUE" and cell_value({}) == "" and cell_value({"a": "b"}) == '{"a": "b"}'
