#!/usr/bin/env python3

import sys
from subprocess import Popen, PIPE

history = []


def start(script, *args):
    return Popen([sys.executable, script, *args], stdin=PIPE, stdout=PIPE,
                 encoding="utf8")


def log(logger, action, message=""):
    logger.stdin.write(f"{action} {message}".rstrip() + "\n")
    logger.stdin.flush()


def ask_enc(enc, line):
    """Send one command line to the encryption program, return (type, text)."""
    enc.stdin.write(line + "\n")
    enc.stdin.flush()
    resp = enc.stdout.readline().rstrip("\n")
    parts = resp.split(" ", 1)
    return parts[0], (parts[1] if len(parts) > 1 else "")


def valid(s):
    return s.isalpha() and s.isascii()


def show_history():
    if not history:
        print("History is empty.")
        return
    print("History:")
    for i, item in enumerate(history, 1):
        print(f"  {i}. {item}")


def choose_string(prompt, record):
    """Let the user pick from history or enter a new string.
    Returns an uppercase valid string, or None if cancelled.
    record=True adds newly entered strings to the history."""
    while True:
        print("\n1) Use a string from the history")
        print("2) Enter a new string")
        print("3) Cancel")
        choice = input("Choice: ").strip()
        if choice == "1":
            if not history:
                print("History is empty.")
                continue
            show_history()
            sel = input("Enter number (or 0 to go back): ").strip()
            if sel == "0":
                continue
            if sel.isdigit() and 1 <= int(sel) <= len(history):
                return history[int(sel) - 1]
            print("Invalid selection.")
        elif choice == "2":
            s = input(prompt).strip()
            if not valid(s):
                print("Error: input must contain only letters.")
                return None
            s = s.upper()
            if record:
                history.append(s)
            return s
        elif choice == "3":
            return None
        else:
            print("Invalid choice.")


def do_password(enc, logger):
    s = choose_string("Enter password: ", record=False)
    if s is None:
        log(logger, "ERROR", "Password command cancelled or invalid input")
        return
    kind, text = ask_enc(enc, f"PASS {s}")
    # The password itself is never logged.
    log(logger, kind, "Passkey set" if kind == "RESULT" else text)
    print("Password set." if kind == "RESULT" else f"Error: {text}")


def do_crypt(enc, logger, name):
    s = choose_string(f"Enter string to {name.lower()}: ", record=True)
    if s is None:
        log(logger, "ERROR", f"{name} cancelled or invalid input")
        return
    log(logger, name, s)
    kind, text = ask_enc(enc, f"{name} {s}")
    log(logger, kind, text)
    if kind == "RESULT":
        history.append(text)
        print(f"Result: {text}")
    else:
        print(f"Error: {text}")


def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: driver.py <logfile>\n")
        sys.exit(1)

    logger = start("logger.py", sys.argv[1])
    enc = start("encryption.py")
    log(logger, "START", "Driver started.")

    menu = "\nCommands: password, encrypt, decrypt, history, quit"
    while True:
        print(menu)
        try:
            cmd = input("> ").strip().lower()
        except EOFError:
            cmd = "quit"
        if cmd:
            log(logger, "COMMAND", cmd)

        if cmd == "password":
            do_password(enc, logger)
        elif cmd == "encrypt":
            do_crypt(enc, logger, "ENCRYPT")
        elif cmd == "decrypt":
            do_crypt(enc, logger, "DECRYPT")
        elif cmd == "history":
            show_history()
            log(logger, "HISTORY", f"Displayed {len(history)} item(s)")
        elif cmd == "quit":
            break
        elif cmd:
            print("Unknown command.")
            log(logger, "ERROR", f"Unknown command: {cmd}")

    log(logger, "EXIT", "Driver exiting.")
    enc.stdin.write("QUIT\n")
    enc.stdin.flush()
    logger.stdin.write("QUIT\n")
    logger.stdin.flush()
    enc.wait()
    logger.wait()


if __name__ == "__main__":
    main()
