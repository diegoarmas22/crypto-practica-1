from basics import to_numbers, to_letters


def encrypt(plaintext: str, k: int) -> str:
    nums = to_numbers(plaintext)
    return to_letters([(x + k) % 26 for x in nums])


def decrypt(ciphertext: str, k: int) -> str:
    nums = to_numbers(ciphertext)
    return to_letters([(y - k) % 26 for y in nums])

print(encrypt("MYSECRETMESSAGE", 3))