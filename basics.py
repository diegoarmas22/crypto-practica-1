from itertools import cycle

def to_numbers(text: str) -> list[int]: #normalised text -> 0..25
    letter_to_num = {
    'A': 0,  'B': 1,  'C': 2,  'D': 3,  'E': 4,  'F': 5,  'G': 6,
    'H': 7,  'I': 8,  'J': 9,  'K': 10, 'L': 11, 'M': 12, 'N': 13,
    'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20,
    'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25
}
    resultado = []
    for letter in text.upper():
        if letter in letter_to_num:
            resultado.append(letter_to_num[letter])
    return resultado

print(to_numbers("Hello, World!"))
#returns: [7, 4, 11, 11, 14, 22, 14, 17, 11, 3]

def to_letters(numbers: list[int]) -> str:
    num_to_letter = {
        0: 'A',  1: 'B',  2: 'C',  3: 'D',  4: 'E',  5: 'F',  6: 'G',
        7: 'H',  8: 'I',  9: 'J',  10: 'K', 11: 'L', 12: 'M', 13: 'N',
        14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U',
        21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'
    }
    resultado = []
    for number in numbers:
        letra = num_to_letter[number % 26]
        resultado.append(letra)
    return "".join(resultado)

print(to_letters([7, 4, 11, 11, 14, 22, 14, 17, 11, 3]))
#returns: 'HELLOWORLD'

def egcd(a: int, b: int) -> tuple[int, int, int]: #finds Bezout coefficients for positive inputs
    prev_coeff_x, current_coeff_x = 1, 0
    prev_coeff_y, current_coeff_y = 0, 1

    prev_remainder, current_remainder = a, b

    while current_remainder != 0:
        quotient = prev_remainder // current_remainder

        # Update remainders
        next_remainder = prev_remainder - quotient * current_remainder
        prev_remainder = current_remainder
        current_remainder = next_remainder

        # Update x coefficients
        next_coeff_x = prev_coeff_x - quotient * current_coeff_x
        prev_coeff_x = current_coeff_x
        current_coeff_x = next_coeff_x

        # Update y coefficients
        next_coeff_y = prev_coeff_y - quotient * current_coeff_y
        prev_coeff_y = current_coeff_y
        current_coeff_y = next_coeff_y

    gcd = prev_remainder
    x = prev_coeff_x
    y = prev_coeff_y

    #if gcd  negative, invert signs to maintain g >= 0
    if gcd < 0:
        return -gcd, -x, -y

    return gcd, x, y

def modinv(a: int, m: int) -> int: #Calculates modular division: finds x where (a * x) % m = 1.
    if m == 0:
        raise ValueError("Modulus cannot be 0")

    modulus = abs(m)
    gcd, inv_x, _ = egcd(a, modulus)

    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    
    return inv_x % modulus
print(modinv(5, 26)) #21


def xor_bytes(data: bytes, key: bytes) -> bytes: #Encrypts/decrypts byte data using a repeating XOR key.
    if not key:
        raise ValueError("Key cannot be empty.")
    return bytes(data_byte ^ key_byte for data_byte, key_byte in zip(data, cycle(key)))
print(xor_bytes(b"HELLO", b"KEYKE").hex())
#returns 030015070a

