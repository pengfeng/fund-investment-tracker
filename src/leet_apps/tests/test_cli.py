from subprocess import Popen, PIPE
import sys
import json


def test_cli_output_json(capsys, tmp_path):
    # Run the CLI with sample fund and capture stdout
    from leet_apps.cli import main

    # Simulate CLI args by calling main() after setting sys.argv
    sys_argv_backup = sys.argv
    try:
        sys.argv = ["fund-tracker", "--fund", "Sequoia Capital"]
        main()
    finally:
        sys.argv = sys_argv_backup


# Note: More comprehensive CLI tests (file output) can be added; this minimal test ensures main() runs
