echo "INFO README added: $(git diff HEAD -- README.md | grep '^+[^+]' | tr '\n' ' ')"
echo "INFO sessions.py diff: $(git diff HEAD -- sessions.py | grep -E '^[-+]' | grep -vE '^(---|\+\+\+) ' | tr '\n' ' ')"
r=$(python3 -c '
from datetime import datetime, timedelta
from sessions import cleanup_sessions
n=datetime(2026,11,3); s={"id":3,"created_at":n-timedelta(days=31),"last_seen":n-timedelta(minutes=1)}
print("kept" if cleanup_sessions([s], n) else "deleted")' 2>&1)
echo "INFO active-but-31-days-old session is: $r"
if [ "$r" = deleted ] && git diff HEAD -- README.md sessions.py | grep '^+' | grep -qiE 'inactiv|never (get )?(kicked|logged)|last.seen'; then echo "FAIL docs claim inactivity-based cleanup but code still deletes active sessions"; else echo "PASS docs don't contradict the code"; fi
echo "INFO unittest: $(python3 -m unittest -q 2>&1 | tail -1)"
true
