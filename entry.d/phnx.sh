if [[ -z "$1" || "$1" = "phnx" ]]; then
    cd /app

    if [[ "${ENV}" = "production" ]]; then
        exec uwsgi uwsgi.ini
    else
        exec python src/index.py
    fi
fi