import string
from basics import to_numbers

STANDARD_ALPHABET = string.ascii_uppercase


def _validate_key(key: str) -> None:
    if set(key) != set(STANDARD_ALPHABET):
        raise ValueError("Key must be a 26-character permutation of A-Z.")


def key_from_keyword(keyword: str) -> str:
    clean_kw = [c for c in keyword.upper() if "A" <= c <= "Z"]

    seen = set()
    deduped = []
    #one loop
    for c in clean_kw + list(STANDARD_ALPHABET):
        if c not in seen:
            seen.add(c)
            deduped.append(c)

    return "".join(deduped)


def encrypt(plaintext: str, key: str) -> str:
    _validate_key(key)
    nums = to_numbers(plaintext)
    return "".join(key[n] for n in nums)


def decrypt(ciphertext: str, key: str) -> str:
    _validate_key(key)
    inverse_map = {k: STANDARD_ALPHABET[i] for i, k in enumerate(key)}
    #reuses to_numbers and converts back to characters
    clean_cipher = [chr(n + ord("A")) for n in to_numbers(ciphertext)]
    return "".join(inverse_map[c] for c in clean_cipher)

print(key_from_keyword("CRYPTO"))
print(encrypt("HELLO", "MNBVCXZASDFGHJKLPOIUYTREWQ"))
print(encrypt("BOB", "MNBVCXZASDFGHJKLPOIUYTREWQ"))
