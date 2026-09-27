from math import gcd
from basics import to_numbers, to_letters, modinv


def valid_keys() -> list[tuple[int, int]]:
    # Coprime with 26: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)
    # Total valid keys: 12 * 26 = 312
    return [(a, b) for a in range(26) if gcd(a, 26) == 1 for b in range(26)]


def encrypt(plaintext: str, a: int, b: int) -> str:
    if gcd(a, 26) != 1:
        raise ValueError
    nums = to_numbers(plaintext)
    return to_letters([(a * x + b) % 26 for x in nums])


def decrypt(ciphertext: str, a: int, b: int) -> str:
    a_inv = modinv(a, 26)
    nums = to_numbers(ciphertext)
    return to_letters([(a_inv * (y - b)) % 26 for y in nums])
print(encrypt("attack", 5, 8))