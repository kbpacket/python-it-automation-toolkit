# Python IT Automation Toolkit

A standard-library Python toolkit for three common entry-level IT tasks:

1. Collecting a system inventory
2. Creating and verifying SHA-256 file-integrity manifests
3. Summarizing structured application logs

This is a hands-on learning project. The emphasis is on safe defaults, readable code, testing, and documentation.

## Skills demonstrated

- Python command-line tools
- JSON input and output
- File hashing and integrity validation
- Log parsing and summary reporting
- Unit testing with \`unittest\`
- Continuous integration with GitHub Actions

## Project structure

\`\`\`text
.
├── .github/workflows/tests.yml
├── examples/sample.log
├── src/
│   ├── file_integrity.py
│   ├── log_summary.py
│   └── system_inventory.py
└── tests/
    ├── test_file_integrity.py
    └── test_log_summary.py
\`\`\`

## Quick start

Python 3.10 or newer is recommended. No third-party packages are required.

\`\`\`bash
python src/system_inventory.py
python src/log_summary.py examples/sample.log
\`\`\`

Create and verify a file-integrity manifest:

\`\`\`bash
python src/file_integrity.py create examples --manifest manifest.json
python src/file_integrity.py verify examples --manifest manifest.json
\`\`\`

Run the tests:

\`\`\`bash
python -m unittest discover -s tests -v
\`\`\`

## Security notes

- Run these scripts only on systems and files you are authorized to inspect.
- Inventory output can contain hostnames and system details. Review it before sharing.
- A matching hash proves that content has not changed since the manifest was created. It does not prove that the original content was safe.
- The toolkit reads data but does not modify monitored files.

## What I learned

- How deterministic output and sorted paths make integrity checks repeatable
- Why useful automation needs clear exit codes and error messages
- How tests protect behavior while code changes
- Why logs and inventory reports should be reviewed for sensitive data

## Next improvements

- Add CSV output for inventory reports
- Support configurable log formats
- Add signed manifests
- Send summaries to a cloud storage test environment
