# Playwright's image ships Chromium and its system libraries in /ms-playwright. The Python
# package must match the image version exactly, or it looks for a browser build that isn't there.
ARG PLAYWRIGHT_VERSION=1.63.0
FROM mcr.microsoft.com/playwright/python:v${PLAYWRIGHT_VERSION}-noble
ARG PLAYWRIGHT_VERSION

WORKDIR /app
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install ".[sheets]" "playwright==${PLAYWRIGHT_VERSION}"

# Outputs land in /app/data; mount a volume there to keep them.
ENTRYPOINT ["wdk"]
CMD ["--help"]
