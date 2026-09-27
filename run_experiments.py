import random
import string
from basics import to_letters, to_numbers
import caesar
import break_caesar
import vigenere
import break_vigenere
import assist

def load_clean_text(filename: str) -> str:
    """Reads a file and converts it to pure A-Z characters."""
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    return to_letters(to_numbers(content))

def run_caesar_experiment(corpus: str, text_lang: str, table_lang: str, lengths: list[int], trials: int = 200) -> dict[int, float]:
    """Runs >= 200 trials for each length and calculates success rate."""
    scores = {}
    for L in lengths:
        successes = 0
        for _ in range(trials):
            #grab a random slice of length L
            start = random.randint(0, len(corpus) - L - 1)
            fragment = corpus[start : start + L]

            #pick a random caesar shift (0 to 25)
            true_key = random.randint(0, 25)

            #encrypt it
            ciphertext = caesar.encrypt(fragment, true_key)

            #try to break it
            guessed_key, _ = break_caesar.break_caesar(ciphertext, language=table_lang)

            #check if it was correct
            if guessed_key == true_key:
                successes += 1

        scores[L] = (successes / trials) * 100.0
    return scores

def run_vigenere_experiment(corpus: str, key_lengths: list[int], text_lengths: list[int], trials: int = 100) -> dict:
    """Runs >= 100 trials for each (m, N) combination."""
    results = {m: {} for m in key_lengths}
    for m in key_lengths:
        for N in text_lengths:
            successes = 0
            for _ in range(trials):
                start = random.randint(0, len(corpus) - N - 1)
                fragment = corpus[start : start + N]

                #generate random key of length m
                true_key = "".join(random.choices(string.ascii_uppercase, k=m))

                #encrypt
                ciphertext = vigenere.encrypt(fragment, true_key)

                #break
                guessed_key, _ = break_vigenere.break_vigenere(ciphertext, m=m, language="en")

                if guessed_key == true_key:
                    successes += 1

            results[m][N] = (successes / trials) * 100.0
    return results

if __name__ == "__main__":
    print("Loading corpora...")
    en_corpus = load_clean_text("corpus_en.txt")
    es_corpus = load_clean_text("corpus_es.txt")

    #experiment C1: caesar breaker
    c1_lengths = [20, 30, 40, 60, 100]
    print(f"\nRunning C1 Caesar experiments (200 trials per cell)...")

    en_en = run_caesar_experiment(en_corpus, "en", "en", c1_lengths, trials=200)
    es_en = run_caesar_experiment(es_corpus, "es", "en", c1_lengths, trials=200)
    es_es = run_caesar_experiment(es_corpus, "es", "es", c1_lengths, trials=200)

    print("\n--- C1 RESULTS ---")
    print(f"{'Length':<8} | {'English text / EN Table':<24} | {'Spanish text / EN Table':<24} | {'Spanish text / ES Table':<24}")
    print("-" * 88)
    for L in c1_lengths:
        print(f"{L:<8} | {en_en[L]:>21.1f}% | {es_en[L]:>21.1f}% | {es_es[L]:>21.1f}%")

    #experiment C3: vigenere breaker
    v_keys = [3, 5, 7]
    v_lengths = [60, 120, 200, 300]
    print(f"\nRunning C3 Vigenere experiments (100 trials per cell)...")

    v_results = run_vigenere_experiment(en_corpus, v_keys, v_lengths, trials=100)

    print("\n--- C3 RESULTS ---")
    header = f"{'Key Length (m)':<15} | " + " | ".join([f"N={N:<5}" for N in v_lengths])
    print(header)
    print("-" * len(header))
    for m in v_keys:
        row = f"{m:<15} | " + " | ".join([f"{v_results[m][N]:>5.1f}%" for N in v_lengths])
        print(row)

#experiment C4: frequency assistant for monoalphabetic substitution

cryptogram = """
QATNT YSMHQ XJOCY HKATM FSNQI TUTMP TKTIP JIDTT KHIGQ ATCEG
JMHQA FNTYM TQRTY CSNTJ IEXQA TDTXY CIRTY ACIGT PVATI HQHNY
JFKMJ FHNTP
"""

print(assist.report(cryptogram, language="en"))