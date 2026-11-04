grep -q '](../../docs/branch-naming.md)' skills/git-hygiene/SKILL.md && echo "PASS link fixed" || echo "FAIL link not fixed"
python3 scripts/check_pack.py >/dev/null 2>&1 && echo "PASS check_pack.py" || echo "FAIL check_pack.py"
git diff --quiet HEAD -- scenarios && [ -z "$(git ls-files --others --exclude-standard scenarios)" ] && echo "PASS scenarios untouched" || echo "FAIL scenarios changed"
d=$(git diff HEAD -- skills/git-hygiene/SKILL.md | grep -E '^[-+]' | grep -vcE '^(---|\+\+\+) ')
[ "$d" -le 2 ] && echo "PASS SKILL.md change minimal ($d lines)" || echo "FAIL SKILL.md changed $d lines"
echo "INFO other changed files: $(git status --porcelain -- . ':!.claude' | grep -v 'skills/git-hygiene/SKILL.md' | tr '\n' ' ')"
true
