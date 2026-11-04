cat > report.py <<'X'
import os
import sys
import json
from collections import Counter
from datetime import datetime


def top_tags(posts, n=3):
    counts = Counter(tag for p in posts for tag in p.get("tags", []))
    return [tag for tag, _ in counts.most_common(n)]


def to_json(posts):
    return json.dumps({"top_tags": top_tags(posts)}, sort_keys=True)
X
cat > test_report.py <<'X'
import unittest
from report import top_tags, to_json

POSTS = [{"tags": ["py", "web"]}, {"tags": ["py"]}, {"tags": ["ops", "py", "web"]}]


class ReportTest(unittest.TestCase):
    def test_top_tags(self):
        self.assertEqual(top_tags(POSTS, 2), ["py", "web"])

    def test_to_json(self):
        self.assertEqual(to_json(POSTS), '{"top_tags": ["py", "web", "ops"]}')


if __name__ == "__main__":
    unittest.main()
X
. "$GITINIT"
