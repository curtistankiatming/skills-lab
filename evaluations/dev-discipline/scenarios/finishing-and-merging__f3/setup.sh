cat > fmt.py <<'X'
def status_line(name, ok):
    return f"{name}: {'ok' if ok else 'FAILED'}"
X
cat > test_fmt.py <<'X'
import unittest
from fmt import status_line


class FmtTest(unittest.TestCase):
    def test_plain(self):
        self.assertEqual(status_line("db", True), "db: ok")
X
echo "__pycache__/" > .gitignore
. "$GITINIT"
git checkout -qb cli-colors
cat > fmt.py <<'X'
GREEN, RED, RESET = "\033[32m", "\033[31m", "\033[0m"


def status_line(name, ok, color=False):
    word = "ok" if ok else "FAILED"
    if color:
        word = (GREEN if ok else RED) + word + RESET
    return f"{name}: {word}"
X
cat >> test_fmt.py <<'X'

    def test_color(self):
        self.assertEqual(status_line("db", False, color=True), "db: \033[31mFAILED\033[0m")
X
git commit -qam "Optional colored status lines"
git checkout -q main
echo "# healthcheck" > README.md
echo "Prints one status line per service." >> README.md
git add README.md && git commit -qm "Add README"
