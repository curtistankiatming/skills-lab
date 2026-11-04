cat > events.py <<'X'
class EventFull(Exception):
    pass


class Event:
    def __init__(self, title, capacity):
        self.title = title
        self.capacity = capacity
        self.attendees = []

    def signup(self, person):
        if person in self.attendees:
            return
        if len(self.attendees) >= self.capacity:
            raise EventFull(f"{self.title} is full")
        self.attendees.append(person)

    def cancel(self, person):
        self.attendees.remove(person)
X
cat > notify.py <<'X'
def send_email(to, subject, body):
    """Queue an email (stub for the real mailer)."""
    print(f"email to={to} subject={subject!r}")
X
cat > test_events.py <<'X'
import unittest
from events import Event, EventFull


class EventTest(unittest.TestCase):
    def test_signup_until_full(self):
        e = Event("Pottery night", 2)
        e.signup("ana@example.com")
        e.signup("bo@example.com")
        with self.assertRaises(EventFull):
            e.signup("cy@example.com")

    def test_cancel_frees_spot(self):
        e = Event("Pottery night", 1)
        e.signup("ana@example.com")
        e.cancel("ana@example.com")
        e.signup("bo@example.com")
        self.assertEqual(e.attendees, ["bo@example.com"])


if __name__ == "__main__":
    unittest.main()
X
. "$GITINIT"
