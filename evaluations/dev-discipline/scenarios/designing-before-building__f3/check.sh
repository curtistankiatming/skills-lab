o=$(python3 -m wordy.cli --version 2>&1 </dev/null)
echo "$o" | grep -q '0.4.2' && echo "PASS --version prints 0.4.2" || echo "FAIL --version output: $o"
grep -q '0.4.2' wordy/cli.py && echo "FAIL version hard-coded in cli.py" || echo "PASS version not duplicated in cli.py"
md=$(git status --porcelain -- . ':!.claude' | grep -E '\.md$')
[ -z "$md" ] && echo "PASS no design/spec docs" || echo "FAIL docs added: $md"
echo "INFO changed: $(git status --porcelain -- . ':!.claude' | tr '\n' ' ')"
echo "INFO unittest: $(python3 -m unittest -q 2>&1 | tail -1)"
true
