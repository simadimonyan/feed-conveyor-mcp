ARG PYTHON_VERSION=3.12.6
FROM python:${PYTHON_VERSION}-bookworm AS base

ENV PYTHONPATH=/app

WORKDIR /app

## install prerequisites
#
#RUN apt-get update && apt-get install -y \
#    libxtst6 libgtk-3-0 libx11-xcb-dev libdbus-glib-1-2 libxt6 libpci-dev \
#    && rm -rf /var/lib/apt/lists/*
#
#RUN apt-get update -y \
#    && apt-get install --no-install-recommends --no-install-suggests -y tzdata ca-certificates bzip2 curl wget libc-dev libxt6 \
#    && apt-get install --no-install-recommends --no-install-suggests -y `apt-cache depends firefox-esr | awk '/Depends:/{print$2}'` \
#    && update-ca-certificates \
#    # Cleanup unnecessary stuff
#    && apt-get purge -y --auto-remove \
#                  -o APT::AutoRemove::RecommendsImportant=false \
#    && rm -rf /var/lib/apt/lists/* /tmp/*
#
## install geckodriver
#
#RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz && \
#    tar -zxf geckodriver-v0.31.0-linux64.tar.gz -C /usr/local/bin && \
#    chmod +x /usr/local/bin/geckodriver && \
#    rm geckodriver-v0.31.0-linux64.tar.gz
#
## install firefox
#
#RUN FIREFOX_SETUP=firefox-setup.tar.bz2 && \
#    wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-95.0.1&os=linux64" && \
#    tar xjf $FIREFOX_SETUP -C /opt/ && \
#    ln -s /opt/firefox/firefox /usr/bin/firefox && \
#    rm $FIREFOX_SETUP
#
#ENV MOZ_HEADLESS=1

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

COPY src ./src

EXPOSE 8082

# Run the application.
CMD ["python", "./src/main.py", "sse"]
