from affine import decrypt, valid_keys
from break_caesar import FREQ_TABLES, chi_squared


def break_affine(
ciphertext: str, language: str = "en") -> tuple[tuple[int, int], str]:
    if language not in FREQ_TABLES:
        raise ValueError(f"Unsupported language: {language}")

    table = FREQ_TABLES[language]
    keys = valid_keys()  # 12 * 26 = 312 candidates

    best_key = (1, 0)
    best_score = float("inf")
    best_plaintext = ""

    for a, b in keys:
        candidate = decrypt(ciphertext, a, b)
        score = chi_squared(candidate, table)
        if score < best_score:
            best_score = score
            best_key = (a, b)
            best_plaintext = candidate

    return best_key, best_plaintext