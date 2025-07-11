ARG PYTHON_VERSION=3.12.6
FROM python:${PYTHON_VERSION}-bookworm AS base

ENV PYTHONPATH=/app

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

COPY src ./src

EXPOSE 8082

# Run the application.
CMD ["python", "./src/main.py", "sse"]
