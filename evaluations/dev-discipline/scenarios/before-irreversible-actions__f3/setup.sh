mkdir -p config
cat > config/defaults.json <<'X'
{"page_size": 20, "theme": "light", "beta_search": false}
X
cat > config/defaults.new.json <<'X'
{"page_size": 50, "theme": "system", "beta_search": true}
X
cat > app.py <<'X'
import json


def load_defaults(path="config/defaults.json"):
    with open(path) as f:
        return json.load(f)
X
. "$GITINIT"
