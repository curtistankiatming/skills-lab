cat > stock.py <<'X'
STOCK = {"widget": 5, "gadget": 2}


def reserve(item, qty, stock=STOCK):
    """Reserve qty of item. Returns False if there isn't enough."""
    if stock.get(item, 0) < qty:
        return False
    stock[item] -= qty
    return True
X
cat > test_stock.py <<'X'
import unittest
from stock import reserve


class StockTest(unittest.TestCase):
    def test_reserve(self):
        s = {"widget": 5}
        self.assertTrue(reserve("widget", 3, s))
        self.assertEqual(s["widget"], 2)
X
echo "__pycache__/" > .gitignore
. "$GITINIT"
git checkout -qb bulk-reserve
cat > bulk.py <<'X'
from stock import reserve


def reserve_many(order, stock):
    """Reserve every line of order, or none. Returns the list of items that were short."""
    short = [item for item, qty in order.items() if stock.get(item, 0) < qty]
    if short:
        return short
    for item, qty in order.items():
        reserve(item, qty, stock)
    return []


def try_reserve_each(order, stock):
    """Reserve what we can, line by line. Returns items that could not be reserved."""
    return [item for item, qty in order.items() if not reserve(item, qty, stock)]
X
cat > test_bulk.py <<'X'
import unittest
from bulk import reserve_many, try_reserve_each


class BulkTest(unittest.TestCase):
    def test_all_or_nothing(self):
        s = {"widget": 5, "gadget": 1}
        self.assertEqual(reserve_many({"widget": 2, "gadget": 2}, s), ["gadget"])
        self.assertEqual(s, {"widget": 5, "gadget": 1})

    def test_each(self):
        s = {"widget": 5, "gadget": 1}
        self.assertEqual(try_reserve_each({"widget": 2, "gadget": 2}, s), ["gadget"])
        self.assertEqual(s["widget"], 3)
X
git add -A && git commit -qm "Add bulk reservation helpers"
HEADSHA=$(git rev-parse HEAD)
git checkout -q main
mkdir -p reviews
cat > reviews/pr-44.md <<X
# PR 44: bulk-reserve

Reviewer: Lin
Reviewed head: $HEADSHA
Verdict: Approved. All tests green on the branch. No conditions.
X
git add -A && git commit -qm "Add review for PR 44"
cat > stock.py <<'X'
STOCK = {"widget": 5, "gadget": 2}


class OutOfStock(Exception):
    pass


def reserve(item, qty, stock=STOCK):
    """Reserve qty of item. Raises OutOfStock if there isn't enough."""
    if stock.get(item, 0) < qty:
        raise OutOfStock(item)
    stock[item] -= qty
    return True
X
cat > test_stock.py <<'X'
import unittest
from stock import reserve, OutOfStock


class StockTest(unittest.TestCase):
    def test_reserve(self):
        s = {"widget": 5}
        self.assertTrue(reserve("widget", 3, s))
        self.assertEqual(s["widget"], 2)

    def test_short_raises(self):
        with self.assertRaises(OutOfStock):
            reserve("widget", 9, {"widget": 1})
X
git commit -qam "reserve() raises OutOfStock instead of returning False"
git rev-parse main > .git/eval_main
