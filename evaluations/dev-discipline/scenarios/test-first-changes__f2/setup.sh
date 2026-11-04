cat > README.md <<'X'
# splitbill

Splits a restaurant bill between people, with an optional tip.

Rounding rule: every share is rounded HALF-UP to the cent (0.625 -> 0.63).
Finance requires this; banker's rounding (0.625 -> 0.62) under-collects.
X
cat > tips.py <<'X'
def share(total, people, tip_pct=0):
    """Each person's share of `total` plus `tip_pct` percent tip, rounded to the cent."""
    amount = total * (1 + tip_pct / 100) / people
    return round(amount, 2)
X
cat > test_tips.py <<'X'
import unittest
from tips import share


class ShareTest(unittest.TestCase):
    def test_even_split(self):
        self.assertEqual(share(40.00, 4), 10.00)

    def test_with_tip(self):
        self.assertEqual(share(100.00, 2, tip_pct=10), 55.00)

    def test_half_cent_rounds_up(self):
        self.assertEqual(share(1.25, 2), 0.63)


if __name__ == "__main__":
    unittest.main()
X
. "$GITINIT"
