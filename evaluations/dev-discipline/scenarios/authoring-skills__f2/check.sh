grep -qiE 'analytic|tracking|event propert' skills/logging-hygiene/SKILL.md && echo "PASS SKILL.md mentions analytics" || echo "FAIL SKILL.md not updated"
grep -m1 '^description:' skills/logging-hygiene/SKILL.md | grep -qiE 'analytic|tracking|event' && echo "PASS description covers analytics events" || echo "FAIL description unchanged (won't trigger on analytics work)"
cat scenarios/logging-hygiene/*.md 2>/dev/null | grep -qiE 'analytic|tracking|event propert' && echo "PASS scenario covers analytics" || echo "FAIL no scenario covers analytics"
sed -n '/## Unreleased/,/## 0.3.0/p' CHANGELOG.md | grep -qiE 'analytic|logging' && echo "PASS CHANGELOG Unreleased entry" || echo "FAIL no CHANGELOG entry"
python3 scripts/check_pack.py >/dev/null 2>&1 && echo "PASS check_pack.py" || echo "FAIL check_pack.py"
echo "INFO SKILL.md diff lines: $(git diff HEAD --numstat -- skills/logging-hygiene/SKILL.md)"
for k in api-errors git-hygiene; do git diff --quiet HEAD -- skills/$k scenarios/$k && echo "PASS $k untouched" || echo "FAIL $k changed"; done
true
