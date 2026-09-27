import string
from collections import Counter
from caesar import decrypt

# Standard letter frequency distributions
# Lewand, Robert (2000), Cryptological Mathematics (english one)
# Pratt, Fletcher (1942), Secret and Urgent (spanish one)
FREQ_TABLES: dict[str, dict[str, float]] = {
    "en": {
        "A": 0.08167,
        "B": 0.01492,
        "C": 0.02782,
        "D": 0.04253,
        "E": 0.12702,
        "F": 0.02228,
        "G": 0.02015,
        "H": 0.06094,
        "I": 0.06966,
        "J": 0.00153,
        "K": 0.00772,
        "L": 0.04025,
        "M": 0.02406,
        "N": 0.06749,
        "O": 0.07507,
        "P": 0.01929,
        "Q": 0.00095,
        "R": 0.05987,
        "S": 0.06327,
        "T": 0.09056,
        "U": 0.02758,
        "V": 0.00978,
        "W": 0.02360,
        "X": 0.00150,
        "Y": 0.01974,
        "Z": 0.00074,
    },
    "es": {
        "A": 0.1253,
        "B": 0.0142,
        "C": 0.0468,
        "D": 0.0586,
        "E": 0.1368,
        "F": 0.0069,
        "G": 0.0101,
        "H": 0.0070,
        "I": 0.0625,
        "J": 0.0044,
        "K": 0.0002,
        "L": 0.0497,
        "M": 0.0315,
        "N": 0.0671,
        "O": 0.0868,
        "P": 0.0251,
        "Q": 0.0088,
        "R": 0.0687,
        "S": 0.0798,
        "T": 0.0463,
        "U": 0.0393,
        "V": 0.0090,
        "W": 0.0001,
        "X": 0.0022,
        "Y": 0.0090,
        "Z": 0.0052,
    },
}

def chi_squared(text: str, table: dict[str, float]) -> float:
    clean = [c for c in text.upper() if "A" <= c <= "Z"]
    n = len(clean)
    if n == 0:
        return float("inf")

    counts = Counter(clean)
    #normalized chi-squared: sum((observed - expected)^2 / expected) / N
    score = 0.0
    for char, expected_prob in table.items():
        expected_count = n * expected_prob
        observed_count = counts[char]
        score += ((observed_count - expected_count) ** 2) / expected_count
    return score / n


def break_caesar(ciphertext: str, language: str = "en") -> tuple[int, str]:
    if language not in FREQ_TABLES:
        raise ValueError

    table = FREQ_TABLES[language]
    best_shift = 0
    best_score = float("inf")
    best_plaintext = ""

    for k in range(26):
        candidate = decrypt(ciphertext, k)
        score = chi_squared(candidate, table)
        if score < best_score:
            best_score = score
            best_shift = k
            best_plaintext = candidate

    return best_shift, best_plaintext