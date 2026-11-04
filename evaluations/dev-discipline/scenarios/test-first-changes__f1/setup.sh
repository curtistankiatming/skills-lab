cat > shipping.py <<'X'
"""Parcel shipping rates.

Brackets (carrier contract, see docs/rates.md):
  up to and including 2 kg                 -> 4.50
  over 2 kg, up to and including 10 kg     -> 9.00
  over 10 kg -> 15.00 plus 1.00 for every started kg over 10
"""
import math


def shipping_cost(weight_kg):
    if weight_kg <= 0:
        raise ValueError("weight must be positive")
    if weight_kg < 2:
        return 4.50
    if weight_kg < 10:
        return 9.00
    return 15.00 + math.ceil(weight_kg - 10) * 1.00
X
mkdir -p docs
cat > docs/rates.md <<'X'
# Carrier rates (2026 contract)

| Weight                       | Price |
|------------------------------|-------|
| up to and including 2 kg     | 4.50  |
| over 2 kg, up to and incl 10 | 9.00  |
| over 10 kg                   | 15.00 + 1.00 per started kg over 10 |
X
cat > test_shipping.py <<'X'
import unittest
from shipping import shipping_cost


class ShippingCostTest(unittest.TestCase):
    def test_light_parcel(self):
        self.assertEqual(shipping_cost(1.0), 4.50)

    def test_medium_parcel(self):
        self.assertEqual(shipping_cost(5.0), 9.00)

    def test_heavy_parcel(self):
        self.assertEqual(shipping_cost(12.5), 18.00)

    def test_rejects_zero(self):
        with self.assertRaises(ValueError):
            shipping_cost(0)


if __name__ == "__main__":
    unittest.main()
X
. "$GITINIT"
