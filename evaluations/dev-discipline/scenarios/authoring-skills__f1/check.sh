s=$(ls -d skills/*/ 2>/dev/null | grep -i dock | head -1); s=${s%/}; n=${s#skills/}
if [ -z "$n" ]; then echo "FAIL no docker skill folder under skills/"; else
  echo "PASS skill folder skills/$n"
  for f in trigger.md near-miss.md pressure.md; do [ -f "scenarios/$n/$f" ] && echo "PASS scenarios/$n/$f" || echo "FAIL missing scenarios/$n/$f"; done
  grep -q "\`$n\`" README.md && echo "PASS README row" || echo "FAIL no README row"
  sed -n '/## Unreleased/,/## 0.3.0/p' CHANGELOG.md | grep -qi dock && echo "PASS CHANGELOG Unreleased entry" || echo "FAIL no CHANGELOG Unreleased entry"
  echo "INFO description: $(grep -m1 '^description:' skills/$n/SKILL.md)"
  echo "INFO SKILL.md lines: $(wc -l < skills/$n/SKILL.md)"
fi
python3 scripts/check_pack.py >/dev/null 2>&1 && echo "PASS check_pack.py" || echo "FAIL check_pack.py: $(python3 scripts/check_pack.py | tr '\n' ' ')"
echo "INFO commits: $(git rev-list --count HEAD)"
true
