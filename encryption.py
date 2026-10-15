#!/usr/bin/env python3

import sys

A = ord("A")


def vigenere(text, key, sign):
    out = []
    for i, ch in enumerate(text):
        shift = ord(key[i % len(key)]) - A
        out.append(chr((ord(ch) - A + sign * shift) % 26 + A))
    return "".join(out)


def reply(kind, text=""):
    sys.stdout.write(f"{kind} {text}\n" if text else f"{kind}\n")
    sys.stdout.flush()


def main():
    passkey = None
    for line in sys.stdin:
        line = line.rstrip("\n")
        parts = line.split(" ", 1)
        command = parts[0].strip().upper()
        arg = parts[1].strip().upper() if len(parts) > 1 else ""

        if command == "QUIT":
            break
        elif command == "PASS":
            if not arg.isalpha() or not arg.isascii():
                reply("ERROR", "Passkey must contain only letters")
            else:
                passkey = arg
                reply("RESULT")
        elif command in ("ENCRYPT", "DECRYPT"):
            if passkey is None:
                reply("ERROR", "Password not set")
            elif not arg.isalpha() or not arg.isascii():
                reply("ERROR", "Input must contain only letters")
            else:
                sign = 1 if command == "ENCRYPT" else -1
                reply("RESULT", vigenere(arg, passkey, sign))
        else:
            reply("ERROR", "Unknown command")


if __name__ == "__main__":
    main()
