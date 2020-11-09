if [[ -z "$1" || "$1" = "test" ]]; then
    cd /app
    exec pynt test
fi