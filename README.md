# Practice 1 — Classical Substitution Ciphers and Their Cryptanalysis

**Student:** Diego Armas  
**Status:** Individual submission  

---

## 1. How to Run Everything

My project is organized around a single unified Command Line Interface (CLI) in `crypto.py`. In order to make testing and cryptanalysis easier, the script was made to support direct command-line arguments as well as standard stream pipelines (`stdin` and `stdout`). This way it allowed input files to be redirected smoothly. All cipher algorithms make sure of standardized character normalization using `basics.py`, deleting non-alphabetic symbols and whitespace at the same time of converting lowercase input to uppercase latin characters.

Below are the verbatim commands required to replicate all tests, ciphers, breakers, and analytical reports across the project:

### Caesar Cipher
```bash
# Encrypt using an explicit key shift
python crypto.py caesar encrypt --key 3 --in message.txt

# Encrypt reading directly from standard input (stdin pipe)
echo "ATTACK AT DAWN" | python crypto.py caesar encrypt --key 3

# Decrypt writing the normalized plaintext to an output file
python crypto.py caesar decrypt --key 3 --in cipher.txt --out plain.txt
```

### Affine Cipher
```bash
# Encrypt using coprime multiplier a=5 and additive shift b=8
python crypto.py affine encrypt -a 5 -b 8 --in message.txt

# Decrypt writing output to plain.txt
python crypto.py affine decrypt -a 5 -b 8 --in cipher.txt --out plain.txt

# Parameter validation check (rejects invalid multiplier sharing factors with 26)
python crypto.py affine encrypt -a 4 -b 7 --in message.txt
```
### Monoalphabetic Substitution Cipher
```bash
# Encrypt using a memorable keyword (removes duplicate letters and fills the rest)
python crypto.py mono encrypt --keyword CRYPTO --in message.txt

# Encrypt using a direct 26-letter permutation key
python crypto.py mono encrypt --key MNBVCXZASDFGHJKLPOIUYTREWQ --in message.txt

# Decrypt using the same keyword
python crypto.py mono decrypt --keyword CRYPTO --in cipher.txt --out plain.txt
```

### Vigenère Cipher
```bash
# Encrypt using a repeating keyword
python crypto.py vigenere encrypt --key LEMON --in message.txt

# Decrypt using the keyword
python crypto.py vigenere decrypt --key LEMON --in cipher.txt --out plain.txt
```

### Automated Breakers and Cryptanalysis Assistant
```bash
# Break Caesar cipher automatically using English letter frequencies
python crypto.py break caesar --in cipher.txt --lang en

# Break Caesar cipher using Spanish letter frequencies
python crypto.py break caesar --in cipher.txt --lang es

# Break Affine cipher across all 312 coprime key pairs
python crypto.py break affine --in cipher.txt --lang en

# Break Vigenère cipher given period length m=5
python crypto.py break vigenere -m 5 --in cipher.txt --lang en

# Run the frequency cryptanalysis assistant on an unknown cryptogram
python crypto.py assist --in cryptogram.txt --lang en
```

### Graded Test Suite Execution
```bash
# Execute the full pytest test suite from the repository root
python3 -m pytest tests/
```

---

## 2. Key Space Size and Reasoning

To evaluate how secure each cipher is against exhaustive search, we must analyze the exact size of their key spaces:

### Caesar Cipher
* **Key Space:** 26
* **Reasoning:**  In the Caesar cipher, encryption is defined as c = (m + k) (mod26). Because arithmetic is evaluated modulo 26 over the standard alphabet, the key shift parameter k can only take an integer value in the finite set {0, 1, 2,..., 25}

### Affine Cipher
* **Key Space:** 312
* **Reasoning:** The Affine cipher maps each character using c = (a x m + b) (mod26). The additive offset b has 26 possible values in Z26. For the message to be decrypted uniquely, the multiplier a must have a modular multiplicative inverse modulo 26, meaning a and 26 must be coprime.

The 12 valid invertible choices for a are {1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25}

 Total keys= 12 x 26 = 312

### Monoalphabetic Substitution Cipher
* **Key Space:** 26!: aprox 4.03x10^26 
* **Reasoning:** In a monoalphabetic cipher, the key is an arbitrary permutation of the 26 alphabet letters. There are 26 possible substitute choices for 'A', 25 remaining for 'B', 24 for 'C', and so on down to 1 choice for 'Z'. This makes 26! possible permutations, makig brute-force search mathematically impossible.

### Vigenère Cipher (with known key length $m$)
* **Key Space:** 26^m
* **Reasoning:** A Vigenère key consists of a sequence of m independent alphabetical characters. Since each position in the key sequence is chosen freely from the 26 letters of the alphabet, the total number of distinct key combinations is 26x26x...x26 = 26^m.

---

## 3. C1 Measurement Table and Analysis

The objective of Experiment C1 was to determine the accuracy of automated frequency analysis when cracking the Caesar cipher across different message lengths, while at the same time also measuring the penalty of using an incompatible language table. Using texts from Project Gutenberg 1-Frankenstein `corpus_en.txt` and 2-Don Quijote `corpus_es.txt` , I executed 200 random trials for each combination of length and language model.

Table 1: Key Recovery Success Rate (%) for Caesar Cipher over 200 Trials
| Length (L) | English text / EN Table | Spanish text / EN Table | Spanish text / ES Table |
| :--- | :--- | :--- | :--- |
| **20** | 94.0% | 70.5% | 99.0% |
| **30** | 98.5% | 78.5% | 99.5% |
| **40** | 100.0% | 79.5% | 99.5% |
| **60** | 100.0% | 86.0% | 98.0% |
| **100** | 100.0% | 93.0% | 99.5% |

### Analysis of Questions:
* **At which length does your breaker become reliable?**  
If we look at the experimental data gathered in Table 1, the breaker becomes highly reliable - 98.5% at length 30 for English text and length 20 for Spanish text. For more than 40 characters, the success rate reaches a perfect score of 100%. However, we can also conlcude that when texts are shorter than 30 characters, the sample size is too small to accurately represent expected natural language distributions. This happens because short words can change the letter counts, so sometimes the wrong shift can accidentally get a lower chi-squared score.
* **How much does the wrong language table actually cost you?**  
  Evaluating Spanish ciphertext with an English reference creates an important performance deficit. At short lengths (L = 20 to 40) , there is a 15.0% to 28.5% drop in accuracy. However, as the text grows to L = 100, the recovery rate increases back up to 93.0%. This occurs because English and Spanish share high-frequency vowels, particularly 'E' and 'A'. Once the text is long enough to establish clear frequency peaks, the algorithm can still identify the primary shift despite differences among less frequent consonants like 'H', 'W', and 'T' versus 'O' and 'S'.

---

## 4. C2 Comparison with C1

When you break an Affine cipher, the algorithm must evaluate 312 potential (a,b) key candidates and not the 26 additive shifts tested in Caesar. Because the key space is twelve times larger, the probability of encountering a false positive, that happens when an incorrect key transforms short, noisy ciphertext into a distribution that randomly resembles English, is much higher. In Experiment C1, Caesar achieved over 98%$ reliability with just 30 characters. For the Affine cipher, yet, this same level of reliability cannot be achieved on such short strings. The Affine breaker requires a longer text sample around 70 and 90 characters so that it can sufficiently reduce sample noise and ensure that the true (a, b) pair scores a lower chi-squared value than the other 311 candidates.

---

## 5. C3 Table and Governing Factor

For experiment C3 I evaluated how the period length m affects the success rate of breaking the Vigenère cipher across different ciphertext lengths N, using 100 independent trials per cell.

Table 2: Key Recovery Success Rate (%) for Vigenère Cipher over 100 Trials
| Key Length (m) | N = 60 | N = 120 | N = 200 | N = 300 |
| :--- | :--- | :--- | :--- | :--- |
| **m = 3** | 76.0% | 99.0% | 100.0% | 100.0% |
| **m = 5** | 31.0% | 85.0% | 100.0% | 100.0% |
| **m = 7** | 6.0% | 45.0% | 88.0% | 96.0% |

### Analysis of the Governing Factor:
The results of this experiment show that the success rate is not controlled by the total ciphertext length N, but strictly by the effective coset length.

A Vigenère cipher functions as m interleaved Caesar ciphers. To break the entire key, every single coset must be solved correctly. If the probability of cracking an individual coset of length Lcoset is p, the overall probability of recovering the entire key is approximately p^m.

When m is increased, the total letters N are divided across more cosets, reducing the sample size in each stream. For example, with N = 60 and m = 7, each coset contains only 8 or 9 characters. At this short length, the individual Caesar recovery rate decreases significantly, making the overall recovery rate across all 7 independent streams to fall to just 6.0%. Only when N expands enough for each coset to exceed the 30–40 character reliability threshold is when the complete key recovery rate return to 100%.

---

## 6. C4 Findings on the Cryptogram

Using the `assist.py` cryptanalysis module on the 110-character cryptogram we could make the following observations:

```
Ciphertext:
QATNT YSMHQ XJOCY HKATM FSNQI TUTMP TKTIP JIDTT KHIGQ ATCEG
JMHQA FNTYM TQRTY CSNTJ IEXQA TDTXY CIRTY ACIGT PVATI HQHNY
JFKMJ FHNTP
```

* **Suggested Mapping Accuracy:**  
  The cryptogram contains 22 different alphabet letters. The frequency rank only managed to map 5 out of the 22 letters correctly (mainly the high-frequency letter 'E' and isolated edge letters).
* **Most Useful**  
  The most valuable line in the output was the repeated trigram detection:  
  `QAT: count=2, positions=[0, 45]`  
  In English text, a repeated trigram appearing at the start of clauses strongly indicates the word **`THE`**. This single deduction immediately cracks three vital letters at once: `Q -> T`, `A -> H`, and `T -> E`.
* **Why Rank Alignment Alone Fails:**  
  In a small sample of only 110 characters, natural sampling variance easily misrepresents letter counts. Letters in the intermediate frequency range (such as 'A', 'I', 'N', 'O', 'R', and 'S') have expected probabilities that differ by only 1% to 2%. This makes specific word choices of a short text tp cause these letters to frequently trade places in rank order, misleading a simple unigram. What actually solves the cipher is structural language analysis: identifying repeated trigrams (like `THE`), recognizing common bigram transitions (`TH`, `HE`, `IN`), spotting double-letter patterns (such as `TT`), and analyzing vowel-consonant structure.

---

## 7. Monoalphabetic Key Space vs. AES-128

Even though the monoalphabetic substitution cipher possesses a key space of 26! that cannot be brute-forced by any modern supercomputer, a human analyst can break it in minutes using the outputs of the C4 assistant tool. The mapping changes the outward letter identities but leaves all underlying statistical properties of the natural language intact, meaning all the letter frequencies, digram relationships, repeated trigrams, and word patterns pass directly into the ciphertext. The cryptanalyst does not search through the 26! keys, but instead only has to exploit the structural redundancy of the plaintext preserved within the ciphertext. 

In contrast,AES-128 has a smaller key space of 2^128  but cannot be broken this way. AES implements Claude Shannon’s principles of confusion and diffusion across manny algorithmic rounds. Through non-linear substitution boxes (SubBytes), byte permutations (ShiftRows), and linear algebraic column mixing (MixColumns), AES makes sure that every bit of ciphertext depends non-linearly on every bit of the plaintext and every bit of the key. This completely destroys any identifiable unigram, bigram, or morphological language patterns, leaving the ciphertext statistically indistinguishable from random noise and forcing an attacker to face the full computational difficulty of the key space.

---

## 8. Limitations

* **Unequal Coset Distribution:** When the ciphertext length N is not an exact multiple of the Vigenère period m, the earliest cosets contain one more character than cosets behind. On very short messages, this creates minor inequalities in recovery reliability across key positions.

* **Vulnerability to Atypical Plaintext:** The automated chi-squared breakers depend strictly on standard natural language letter distributions. When plaintext deliberately omits high-frequency letters, the chi-squared scoring will identify an incorrect shift key.

* **Degenerate Inputs:** Messages that consist entirely of punctuation, digits, or whitespace normalize to empty strings via `basics.py`, returning empty ciphertexts without error.

---

## 9. Declaration of LLM Assistance


* **Tool Used:** Gemini 
* **Parts Where Assistance Was Used:**
  * **Debugging and Setup:** Assisting with syntax errors in `basics.py` (resolving an early loop return in `to_letters`), handling module import paths, and debugging the `run_experiments.py` script setup.
  * **Theoretical Clarifications:** Explaining the modular arithmetic conditions for the Affine key space and clarifying Shannon's principles of confusion and diffusion versus monoalphabetic substitution for Section 7.

* **What I Did and Changed:**
  * All code execution, testing, and script runs were performed locally on my machine.
  * I ran the experiment simulation scripts (`run_experiments.py`) to generate the experimental numbers, collected the percentage data, and created the C1 and C3 result tables with my own experimental results.
  * I analyzed the C4 cryptogram using `assist.py`, read the output lines, and manually verified the true plaintext decryption to calculate the 5/22 accuracy of the suggested rank alignment.
  * I revised and adjusted the written analysis across all report sections to ensure the tone, structure, and reflections accurately reflect my own work and findings.
