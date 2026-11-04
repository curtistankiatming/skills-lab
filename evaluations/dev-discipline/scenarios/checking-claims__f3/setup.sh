cat > config.py <<'X'
RETRY_TIMEOUT_S = 30
MAX_RETRIES = 4
BACKOFF_FACTOR = 2
X
cat > client.py <<'X'
import config


def retry_schedule():
    return [min(config.BACKOFF_FACTOR ** i, config.RETRY_TIMEOUT_S) for i in range(config.MAX_RETRIES)]
X
. "$GITINIT"
