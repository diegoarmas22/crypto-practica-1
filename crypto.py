import argparse
import sys
import affine
import assist
import break_affine
import break_caesar
import break_vigenere
import caesar
import monoalpha
import vigenere


def get_input(in_path: str | None) -> str: #read from standard input when --in is absent
    if in_path:
        with open(in_path, "r", encoding="utf-8") as f:
            return f.read()
    return sys.stdin.read()


def send_output(content: str, out_path: str | None) -> None:#write to standard output when --out is absent
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content + ("\n" if not content.endswith("\n") else ""))
    else:
        if content.endswith("\n"):
            sys.stdout.write(content)
        else:
            print(content)


def main(): #reads terminal flags according to exact command syntax from the assignment specification
    parser = argparse.ArgumentParser(
        description="Classical Substitution Ciphers CLI",
        add_help=False, 
    )

    #positional commands
    parser.add_argument("cipher", help="Cipher or tool to use")
    parser.add_argument("mode", nargs="?", default=None, help="Mode of operation")

    #key arguments
    parser.add_argument("--key", type=str, default=None)
    parser.add_argument("-a", type=int, default=None)
    parser.add_argument("-b", type=int, default=None)
    parser.add_argument("--keyword", type=str, default=None)
    parser.add_argument("-m", type=int, default=None)

    # I/O and language
    parser.add_argument("--in", dest="in_file", type=str, default=None)
    parser.add_argument("--out", dest="out_file", type=str, default=None)
    parser.add_argument("--lang", choices=["en", "es"], default="en")

    try:
        args = parser.parse_args()
        raw_text = get_input(args.in_file)
        result = ""

        #1)caesar
        if args.cipher == "caesar":
            if args.key is None:
                raise ValueError("Caesar requires --key <int>.")
            k = int(args.key)
            if args.mode == "encrypt":
                result = caesar.encrypt(raw_text, k)
            elif args.mode == "decrypt":
                result = caesar.decrypt(raw_text, k)
            else:
                raise ValueError(f"Unknown mode '{args.mode}' for caesar.")

        #2)affine
        elif args.cipher == "affine":
            if args.a is None or args.b is None:
                raise ValueError("Affine requires both -a <int> and -b <int>.")
            if args.mode == "encrypt":
                result = affine.encrypt(raw_text, args.a, args.b)
            elif args.mode == "decrypt":
                result = affine.decrypt(raw_text, args.a, args.b)
            else:
                raise ValueError(f"Unknown mode '{args.mode}' for affine.")

        #3)monoalphabetic
        elif args.cipher == "mono":
            if args.keyword:
                key = monoalpha.key_from_keyword(args.keyword)
            elif args.key:
                key = args.key
            else:
                raise ValueError("Monoalphabetic cipher requires --key or --keyword.")

            if args.mode == "encrypt":
                result = monoalpha.encrypt(raw_text, key)
            elif args.mode == "decrypt":
                result = monoalpha.decrypt(raw_text, key)
            else:
                raise ValueError(f"Unknown mode '{args.mode}' for mono.")

        #4)vigenere
        elif args.cipher == "vigenere":
            if not args.key:
                raise ValueError("Vigenère requires --key <str>.")
            if args.mode == "encrypt":
                result = vigenere.encrypt(raw_text, args.key)
            elif args.mode == "decrypt":
                result = vigenere.decrypt(raw_text, args.key)
            else:
                raise ValueError(f"Unknown mode '{args.mode}' for vigenere.")

        #5)breakers
        elif args.cipher == "break":
            if args.mode == "caesar":
                shift, pt = break_caesar.break_caesar(raw_text, language=args.lang)
                result = f"Recovered shift: {shift}\nPlaintext:\n{pt}"
            elif args.mode == "affine":
                (a, b), pt = break_affine.break_affine(raw_text, language=args.lang)
                result = f"Recovered key: a={a}, b={b}\nPlaintext:\n{pt}"
            elif args.mode == "vigenere":
                if args.m is None:
                    raise ValueError("Vigenère breaker requires key length: -m <int>.")
                key, pt = break_vigenere.break_vigenere(raw_text, m=args.m, language=args.lang)
                result = f"Recovered key: {key}\nPlaintext:\n{pt}"
            else:
                raise ValueError(f"Unknown breaker target '{args.mode}'.")

        #6)assist
        elif args.cipher == "assist":
            result = assist.report(raw_text, language=args.lang)

        else:
            raise ValueError(f"Unrecognized command or cipher '{args.cipher}'.")

        send_output(result, args.out_file)

    except Exception as e:
        #exit with a non-zero status and a readable message, preventing stack traces
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()