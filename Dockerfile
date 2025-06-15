FROM python:3.12.11-alpine3.22

RUN apk add --no-cache sqlite

RUN adduser --disabled-password --gecos "" strong_language_user

WORKDIR /app

# Copy the whole api directory, not just its contents
COPY api /app/api
COPY requirements.txt /app/
COPY scripts/*.sh /app/scripts/
COPY database/*.sql /app/database/

RUN mkdir -p /app/database && \
    chown -R strong_language_user:strong_language_user /app/database

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=strong_language_user:strong_language_user scripts/init_db.sh /app/init_db.sh
RUN chmod +x /app/init_db.sh

USER strong_language_user

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8000/ || exit 1

CMD ["/app/init_db.sh"]
