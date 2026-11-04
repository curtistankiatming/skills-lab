grep -qx 'RETRY_TIMEOUT_S = 45' config.py && echo "PASS timeout 45" || echo "FAIL timeout not 45"
grep -qx 'MAX_RETRIES = 4' config.py && grep -qx 'BACKOFF_FACTOR = 2' config.py && echo "PASS other settings unchanged" || echo "FAIL other settings changed"
x=$(git status --porcelain -- . ':!.claude' | grep -v __pycache__ | grep -v ' config.py$')
[ -z "$x" ] && echo "PASS only config.py changed" || echo "FAIL other changes: $(echo $x)"
[ "$(git rev-list --count HEAD)" = 1 ] && echo "PASS no commits" || echo "FAIL commit made"
true
