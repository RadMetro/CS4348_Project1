#!/usr/bin/env python3

import sys
from datetime import datetime


def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: logger.py <logfile>\n")
        sys.exit(1)

    with open(sys.argv[1], "a", encoding="utf8") as log:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            parts = line.split(None, 1)
            action = parts[0]
            message = parts[1] if len(parts) > 1 else ""
            if action == "QUIT":
                break
            stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            entry = f"{stamp} [{action}]"
            if message:
                entry += f" {message}"
            log.write(entry + "\n")
            log.flush()


if __name__ == "__main__":
    main()
