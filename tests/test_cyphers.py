from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import affine
import basics
import break_affine
import break_caesar
import break_vigenere
import caesar
import monoalpha
import pytest
import vigenere

import pytest
import basics
import caesar
import affine
import monoalpha
import vigenere
import break_caesar
import break_affine
import break_vigenere

#1)check Values from Handout

def test_published_modinv():
    assert basics.modinv(5, 26) == 21
    assert basics.modinv(7, 26) == 15
    assert basics.modinv(17, 26) == 23
    with pytest.raises(ValueError):
        basics.modinv(13, 26)
    with pytest.raises(ValueError):
        basics.modinv(2, 26)

def test_published_xor_bytes():
    res = basics.xor_bytes(b"HELLO", b"KEYKE").hex()
    assert res == "030015070a"

def test_published_caesar():
    assert caesar.encrypt("MYSECRETMESSAGE", 3) == "PBVHFUHWPHVVDJH"

def test_published_affine():
    assert affine.encrypt("attack", 5, 8) == "IZZISG"
    assert affine.decrypt("IZZISG", 5, 8) == "ATTACK"

def test_published_mono():
    kw_key = monoalpha.key_from_keyword("CRYPTO")
    assert kw_key == "CRYPTOABDEFGHIJKLMNQSUVWXZ"
    
    key = "MNBVCXZASDFGHJKLPOIUYTREWQ"
    assert monoalpha.encrypt("HELLO", key) == "ACGGK"
    assert monoalpha.encrypt("BOB", key) == "NKN"

def test_published_vigenere():
    assert vigenere.encrypt("MYSECRETMESSAGE", "KEY") == "WCQOGPOXKOWQKKC"
    assert vigenere.encrypt("attackatdawn", "LEMON") == "LXFOPVEFRNHR"
    assert vigenere.cosets("ABCDEF", 3) == ["AD", "BE", "CF"]

#2)round-trip correctness: decrypt(encrypt(m, k), k) returns the normalised plaintext

SAMPLE_TEXTS = [
    "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG",
    "ATTACKATDAWN",
    "CRYPTOGRAPHYISINTERESTINGANDPOWERFUL"
]

@pytest.mark.parametrize("m", SAMPLE_TEXTS)
def test_roundtrip_caesar(m):
    for k in [0, 3, 25, 42, -5]:
        assert caesar.decrypt(caesar.encrypt(m, k), k) == m

@pytest.mark.parametrize("m", SAMPLE_TEXTS)
def test_roundtrip_affine(m):
    for a, b in [(1, 0), (3, 7), (5, 8), (11, 21), (25, 25)]:
        assert affine.decrypt(affine.encrypt(m, a, b), a, b) == m

@pytest.mark.parametrize("m", SAMPLE_TEXTS)
def test_roundtrip_mono(m):
    keys = [
        "MNBVCXZASDFGHJKLPOIUYTREWQ",
        monoalpha.key_from_keyword("SECRET"),
        monoalpha.key_from_keyword("CRYPTOGRAPHY")
    ]
    for key in keys:
        assert monoalpha.decrypt(monoalpha.encrypt(m, key), key) == m

@pytest.mark.parametrize("m", SAMPLE_TEXTS)
def test_roundtrip_vigenere(m):
    for key in ["KEY", "LEMON", "VERYLONGKEYWORD"]:
        assert vigenere.decrypt(vigenere.encrypt(m, key), key) == m

#3) rejection of invalid keys: (A, B2, B3, B4)


def test_invalid_keys_basics():
    with pytest.raises(ValueError):
        basics.modinv(2, 26)
    with pytest.raises(ValueError):
        basics.xor_bytes(b"DATA", b"")

def test_invalid_keys_affine():
    with pytest.raises(ValueError):
        affine.encrypt("HELLO", 2, 5)  # gcd(2, 26) != 1
    with pytest.raises(ValueError):
        affine.encrypt("HELLO", 13, 1) # gcd(13, 26) != 1
    with pytest.raises(ValueError):
        affine.decrypt("HELLO", 0, 5)

def test_invalid_keys_mono():
    with pytest.raises(ValueError):
        monoalpha.encrypt("HELLO", "SHORTKEY")
    with pytest.raises(ValueError):
        # 26 chars but duplicate 'A' and missing 'Z'
        monoalpha.encrypt("HELLO", "ABCDEFGHIJKLMNOPQRSTUVWXYA")

def test_invalid_keys_vigenere():
    with pytest.raises(ValueError):
        vigenere.encrypt("HELLO", "")
    with pytest.raises(ValueError):
        vigenere.encrypt("HELLO", "KEY123!")

#4) edge cases: empty, single char, punctuation-only, shorter than Key

def test_edge_cases():
    key_mono = "MNBVCXZASDFGHJKLPOIUYTREWQ"

    #empty 
    assert caesar.encrypt("", 3) == ""
    assert affine.encrypt("", 5, 8) == ""
    assert monoalpha.encrypt("", key_mono) == ""
    assert vigenere.encrypt("", "KEY") == ""

    #single character
    assert caesar.decrypt(caesar.encrypt("A", 5), 5) == "A"
    assert affine.decrypt(affine.encrypt("Z", 7, 3), 7, 3) == "Z"
    assert monoalpha.decrypt(monoalpha.encrypt("M", key_mono), key_mono) == "M"
    assert vigenere.decrypt(vigenere.encrypt("K", "LONGKEY"), "LONGKEY") == "K"

    #no letters at all
    assert caesar.encrypt("12345!@#$ ... ", 3) == ""
    assert affine.encrypt("??!! 992", 5, 8) == ""
    assert monoalpha.encrypt("---", key_mono) == ""
    assert vigenere.encrypt("12345", "KEY") == ""

    #shorter than key
    assert vigenere.decrypt(vigenere.encrypt("HI", "LONGERKEY"), "LONGERKEY") == "HI"

#5)breakers recovering ground truth: at least 20 generated ciphertexts of a length where you claim it is reliable

CORPUS_SAMPLE = (
    "CRYPTOGRAPHYISNOTJUSTABOUTBUILDINGSANDFORTSOFMATHBUTALSOABOUTUNDERSTANDING"
    "THEUNDERLYINGSTATISTICALPROPERTIESOFLANGUAGEANDUSINGTHEMTOEXTRACTSECRETS"
    "WITHOUTHAVINGACCESSTOTHEORIGINALSECRETKEYATALLTIMES"
)

def test_breaker_caesar_reliability():
    #reliable when length >= 60
    frag = CORPUS_SAMPLE[:100]
    for k in range(20):
        ct = caesar.encrypt(frag, k)
        recovered_k, _ = break_caesar.break_caesar(ct, language="en")
        assert recovered_k == k

def test_breaker_affine_reliability():
    #reliable when length >= 80
    frag = CORPUS_SAMPLE[:120]
    valid = affine.valid_keys()[:20]
    for a, b in valid:
        ct = affine.encrypt(frag, a, b)
        (rec_a, rec_b), _ = break_affine.break_affine(ct, language="en")
        assert (rec_a, rec_b) == (a, b)

def test_breaker_vigenere_reliability():
    #reliable with coset length >= 50 
    text = (CORPUS_SAMPLE * 3)[:180]
    keys = ["KEY", "RED", "FOX", "SUN", "SKY"]
    for _ in range(4):
        for k in keys:
            ct = vigenere.encrypt(text, k)
            rec_k, _ = break_vigenere.break_vigenere(ct, m=len(k), language="en")
            assert rec_k == k