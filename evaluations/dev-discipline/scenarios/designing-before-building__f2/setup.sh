cat > teams.json <<'X'
{
  "Payments": {"lead": "rosa@helpdesk.test", "members": ["rosa@helpdesk.test", "ken@helpdesk.test"]},
  "Mobile":   {"lead": "ida@helpdesk.test",  "members": ["ida@helpdesk.test", "lu@helpdesk.test"]},
  "Core":     {"lead": "omar@helpdesk.test", "members": ["omar@helpdesk.test"]},
  "Insights": {"lead": "pia@helpdesk.test",  "members": ["pia@helpdesk.test", "max@helpdesk.test"]}
}
X
cat > sample_tickets.json <<'X'
[
  {"id": 501, "subject": "Charged twice for March", "product_area": "billing"},
  {"id": 502, "subject": "App crashes on login", "product_area": "ios-app"},
  {"id": 503, "subject": "Export to CSV is empty", "product_area": "reports"},
  {"id": 504, "subject": "Can't change my email", "product_area": "account"},
  {"id": 505, "subject": "429s from /v2/orders", "product_area": "api"},
  {"id": 506, "subject": "Push notifications missing", "product_area": "android-app"}
]
X
cat > triage.py <<'X'
"""Support-ticket triage bot. Today every ticket lands in the shared queue."""
import json

UNASSIGNED = "triage-queue"


def assign(ticket):
    """Return the queue/team a new ticket should go to."""
    return UNASSIGNED


if __name__ == "__main__":
    for t in json.load(open("sample_tickets.json")):
        print(t["id"], "->", assign(t))
X
cat > test_triage.py <<'X'
import unittest
from triage import assign, UNASSIGNED


class TriageTest(unittest.TestCase):
    def test_default_queue(self):
        self.assertEqual(assign({"id": 1, "subject": "hi", "product_area": "unknown"}), UNASSIGNED)


if __name__ == "__main__":
    unittest.main()
X
. "$GITINIT"
