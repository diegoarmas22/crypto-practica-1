from itertools import cycle
from basics import to_numbers, to_letters


def _normalize_key(key: str) -> list[int]:
    if not key or not all("A" <= c <= "Z" or "a" <= c <= "z" for c in key):
        raise ValueError
    return to_numbers(key)


def encrypt(plaintext: str, key: str) -> str:
    key_nums = _normalize_key(key)
    plain_nums = to_numbers(plaintext)
    return to_letters(
        [(p + k) % 26 for p, k in zip(plain_nums, cycle(key_nums))]
    )


def decrypt(ciphertext: str, key: str) -> str:
    key_nums = _normalize_key(key)
    cipher_nums = to_numbers(ciphertext)
    return to_letters(
        [(c - k) % 26 for c, k in zip(cipher_nums, cycle(key_nums))]
    )


def cosets(ciphertext: str, m: int) -> list[str]:
    clean_text = "".join(c for c in ciphertext.upper() if "A" <= c <= "Z")
    return [clean_text[i::m] for i in range(m)]

print(encrypt("MYSECRETMESSAGE", "KEY")) #WCQOGPOXKOWQKKC
print(encrypt("attackatdawn", "LEMON")) #LXFOPVEFRNHR
print(cosets("ABCDEF", 3)) 