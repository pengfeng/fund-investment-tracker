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


def test_cli_writes_json_file(tmp_path):
    from leet_apps.cli import main
    p = tmp_path / "out"
    sys_argv_backup = sys.argv
    try:
        sys.argv = ["fund-tracker", "--fund", "Sequoia Capital", "--output", str(p), "--format", "json"]
        main()
        out_file = p.with_suffix('.json')
        assert out_file.exists()
        content = out_file.read_text()
        assert '"fund"' in content or 'companies' in content
    finally:
        sys.argv = sys_argv_backup


def test_cli_writes_csv_files(tmp_path):
    from leet_apps.cli import main
    p = tmp_path / "out"
    sys_argv_backup = sys.argv
    try:
        sys.argv = ["fund-tracker", "--fund", "Sequoia Capital", "--output", str(p), "--format", "csv"]
        main()
        comp = str(p) + "_companies.csv"
        inv = str(p) + "_investments.csv"
        assert comp and inv
        assert open(comp).read()
        assert open(inv).read()
    finally:
        sys.argv = sys_argv_backup
