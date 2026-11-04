mkdir -p wordy
cat > wordy/__init__.py <<'X'
__version__ = "0.4.2"
X
cat > wordy/cli.py <<'X'
import argparse
import sys


def count_words(text):
    return len(text.split())


def main(argv=None):
    parser = argparse.ArgumentParser(prog="wordy", description="Count words in a file.")
    parser.add_argument("path", nargs="?", help="file to read (default: stdin)")
    args = parser.parse_args(argv)
    text = open(args.path).read() if args.path else sys.stdin.read()
    print(count_words(text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
X
cat > test_cli.py <<'X'
import io
import unittest
from contextlib import redirect_stdout
from wordy.cli import count_words, main


class CliTest(unittest.TestCase):
    def test_count(self):
        self.assertEqual(count_words("a b  c\n"), 3)

    def test_main_reads_file(self):
        with open("_t.txt", "w") as f:
            f.write("one two")
        buf = io.StringIO()
        with redirect_stdout(buf):
            main(["_t.txt"])
        self.assertEqual(buf.getvalue().strip(), "2")


if __name__ == "__main__":
    unittest.main()
X
echo "_t.txt" > .gitignore
echo "__pycache__/" >> .gitignore
. "$GITINIT"
