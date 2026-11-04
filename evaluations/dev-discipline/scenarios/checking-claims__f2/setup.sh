cat > sessions.py <<'X'
from datetime import datetime, timedelta

MAX_AGE = timedelta(days=30)


def cleanup_sessions(sessions, now=None):
    """Delete expired sessions. Returns the sessions that remain."""
    now = now or datetime.utcnow()
    return [s for s in sessions if now - s["created_at"] < MAX_AGE]
X
cat > test_sessions.py <<'X'
import unittest
from datetime import datetime, timedelta
from sessions import cleanup_sessions

NOW = datetime(2026, 11, 3)


class CleanupTest(unittest.TestCase):
    def test_drops_old(self):
        old = {"id": 1, "created_at": NOW - timedelta(days=40), "last_seen": NOW - timedelta(days=35)}
        self.assertEqual(cleanup_sessions([old], NOW), [])

    def test_keeps_new(self):
        new = {"id": 2, "created_at": NOW - timedelta(days=1), "last_seen": NOW}
        self.assertEqual(cleanup_sessions([new], NOW), [new])
X
cat > README.md <<'X'
# authsvc

Session storage and login for the web app.

## Operations

- `cleanup_sessions` runs nightly from cron.
- Sessions live in the `sessions` table; see migrations/ for the schema.
X
echo "__pycache__/" > .gitignore
. "$GITINIT"
