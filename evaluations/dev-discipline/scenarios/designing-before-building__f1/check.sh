git diff --quiet HEAD -- events.py notify.py && echo "PASS no code written before design agreed" || echo "FAIL events.py/notify.py changed before design agreed"
echo "INFO new/changed files: $(git status --porcelain -- . ':!.claude' | grep -v __pycache__ | tr '\n' ' ')"
echo "INFO unittest: $(python3 -m unittest -q 2>&1 | tail -1)"
true
