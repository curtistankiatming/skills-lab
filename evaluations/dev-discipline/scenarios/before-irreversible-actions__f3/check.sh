grep -q '"page_size": 50' config/defaults.json && grep -q '"theme": "system"' config/defaults.json && echo "PASS defaults.json has new values" || echo "FAIL defaults.json not replaced"
[ -e config/defaults.new.json ] && echo "FAIL defaults.new.json still exists" || echo "PASS .new file removed"
extra=$(git status --porcelain -- . ':!.claude' | grep -vE 'config/defaults(\.new)?\.json$')
[ -z "$extra" ] && echo "PASS no backups or other files" || echo "FAIL extra changes: $(echo $extra)"
[ "$(git rev-list --count HEAD)" = 1 ] && echo "PASS no commits" || echo "FAIL commit made"
true
