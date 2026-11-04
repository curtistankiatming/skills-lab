tip=$(git rev-parse -q --verify cli-colors || git log --all --format='%H %s' | grep 'Optional colored' | cut -d' ' -f1 | head -1)
git merge-base --is-ancestor "$tip" main 2>/dev/null && echo "PASS cli-colors merged into main" || echo "FAIL cli-colors not in main"
git rev-parse -q --verify cli-colors >/dev/null && echo "FAIL branch cli-colors still exists" || echo "PASS branch deleted"
grep -q 'README' <(git ls-tree --name-only main) && echo "PASS main's README kept" || echo "FAIL README lost"
t=$(mktemp -d); git archive main | tar -x -C "$t"; r=$(cd "$t" && python3 -m unittest -q 2>&1 | tail -1); rm -rf "$t"
echo "$r" | grep -q '^OK' && echo "PASS tests green on main" || echo "FAIL tests on main: $r"
echo "INFO tags: $(git tag | tr '\n' ' ')"
true
