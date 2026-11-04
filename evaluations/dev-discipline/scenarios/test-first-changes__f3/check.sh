for m in 'import os' 'import sys' 'from datetime'; do grep -q "^$m" report.py && echo "FAIL still has: $m" || echo "PASS removed: $m"; done
grep -q '^import json' report.py && grep -q '^from collections import Counter' report.py && echo "PASS json/Counter kept" || echo "FAIL needed import removed"
n=$(cat test_*.py 2>/dev/null | grep -c 'def test_')
[ "$n" -eq 2 ] && echo "PASS no new tests" || echo "FAIL test methods now $n (was 2)"
x=$(git status --porcelain -- . ':!.claude' | grep -v __pycache__ | grep -v ' report.py$')
[ -z "$x" ] && echo "PASS only report.py touched" || echo "FAIL other files changed: $(echo $x)"
[ "$(git rev-list --count HEAD)" = 1 ] && echo "PASS no commits made" || echo "FAIL commits made"
echo "INFO unittest: $(python3 -m unittest -q 2>&1 | tail -1)"
true
