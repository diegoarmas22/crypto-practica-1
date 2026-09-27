from basics import to_letters
from break_caesar import break_caesar
from vigenere import cosets, decrypt


def break_vigenere(ciphertext: str, m: int, language: str = "en") -> tuple[str, str]:
    """m is the key length, given to you. Returns (key, plaintext).
    """
    clean = "".join(c for c in ciphertext.upper() if "A" <= c <= "Z")
    interleaved_cosets = cosets(clean, m)

    # Solve each interleaved Caesar stream independently
    shifts = []
    for coset in interleaved_cosets:
        shift, _ = break_caesar(coset, language=language)
        shifts.append(shift)

    key = to_letters(shifts)
    plaintext = decrypt(clean, key)
    return key, plaintext