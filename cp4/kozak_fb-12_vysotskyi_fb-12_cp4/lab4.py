from random import randint
from typing import Tuple


class PrivateKey:

    def __init__(self, d, p, q):
        self.d = d
        self.p = p
        self.q = q

    def __repr__(self):
        return f"d={self.d}, p={self.p}, q={self.q}"


class PublicKey:

    def __init__(self, n, e):
        self.n = n
        self.e = e

    def __repr__(self):
        return f"n={self.n}, e={self.e}"


def extended_euclid(a, b):   # Розширений алгоритм Евкліда
    """ Повертає d=НСД(x,y) і x, y такі, що ax + by = d """
    if b == 0:
        return a, 1, 0
    d, x, y = extended_euclid(b, a % b)
    return d, y, x - (a // b) * y


def mod_inverse(a, m):
    """Повертає число, обернене до числа a за модулем m"""
    gcd, x, y = extended_euclid(a, m)
    if gcd == 1:
        return x % m
    else:
        return None


def decimal_to_binary(a: int) -> str:
    binary_a = ""
    while a > 0:
        remainder = a % 2
        binary_a = str(remainder) + binary_a
        a //= 2
    return binary_a if binary_a else "0"


def horner_power(base: int, power: int, mod: int) -> int:
    """base ^ power (mod mod)"""
    result = 1
    binary_a = decimal_to_binary(power)

    for bit in binary_a:
        result = (result * result) % mod
        if bit == '1':
            result = (result * base) % mod

    return result


def distribute_number(number) -> Tuple[int, int]:
    p_minus = number - 1
    s = 0
    while p_minus % 2 == 0:
        s += 1
        p_minus //= 2
    d = p_minus
    return d, s


def test_prime_miller_rabin(prime_candidate) -> bool:

    # Крок 0. Знаходимо розклад s p-1 = d * s^2 та встановлюємо лічильник у 0.
    k = 10
    tests_count = 0
    if prime_candidate % 2 == 0:
        return False
    d, s = distribute_number(prime_candidate)
    while tests_count < k:
        # Step 1
        x = randint(2, prime_candidate-1)
        gcd, _, _ = extended_euclid(x, prime_candidate)
        if gcd > 1:
            return False

        # Step 2.1
        if horner_power(x, d, prime_candidate) in (1, -1, prime_candidate-1, prime_candidate+1):
            tests_count += 1
            continue
        # Step 2.2
        x_r = horner_power(x, d, prime_candidate)
        for r in range(1, s):
            x_r = (x_r * x_r) % prime_candidate
            if x_r in (-1, prime_candidate-1):  # Strongly pseudo-prime
                break
            elif x_r == 1:  # Weakly pseudo-prime
                return False
        # Step 2.3
        else:  # Weakly pseudo-prime
            return False

        tests_count += 1
    else:  # Step 3
        return True


def generate_prime_number(lowest: int, highest: int) -> int:
    candidates = []
    while True:
        p = randint(lowest, highest)
        if test_prime_miller_rabin(p):
            print(candidates[:10])
            return p
        else:
            candidates.append(p)


def generate_key_pair(p: int, q: int, e=2 ** 16 + 1) -> Tuple[PrivateKey, PublicKey]:
    n = p*q
    euler = (p-1)*(q-1)

    d = mod_inverse(e, euler)
    return PrivateKey(d, p, q), PublicKey(n, e)


def encrypt(open_text: int, public_key: PublicKey) -> int:
    return horner_power(open_text, public_key.e, public_key.n)


def decrypt(encrypted_text: int, private_key: PrivateKey) -> int:
    n = private_key.p * private_key.q
    return horner_power(encrypted_text, private_key.d, n)


def sign(open_text: int, private_key: PrivateKey) -> Tuple[int, int]:
    n = private_key.p * private_key.q
    signature = horner_power(open_text, private_key.d, n)
    return open_text, signature


def verify(signed_text: Tuple[int, int], public_key: PublicKey) -> bool:
    open_text, signature = signed_text
    return horner_power(signature, public_key.e, public_key.n) == open_text


def send_key(k: int, my_private_key: PrivateKey, their_public_key: PublicKey) -> Tuple[int, int]:
    n = my_private_key.p * my_private_key.q
    s = horner_power(k, my_private_key.d, n)
    s1 = horner_power(s, their_public_key.e, their_public_key.n)
    k1 = horner_power(k, their_public_key.e, their_public_key.n)
    return k1, s1


def receive_key(key_message: Tuple[int, int], my_private_key: PrivateKey, their_public_key: PublicKey) -> int:
    n = my_private_key.p * my_private_key.q
    k1, s1 = key_message
    k = horner_power(k1, my_private_key.d, n)
    s = horner_power(s1, my_private_key.d, n)
    if horner_power(s, their_public_key.e, their_public_key.n) == k:
        return k
    return 0


def run_tests():
    assert distribute_number(13)[0] == 3
    assert distribute_number(13)[1] == 2
    assert distribute_number(100)[1] == 0

    assert horner_power(10, 2, 101) == 100
    assert horner_power(4, 7, 451) == 148

    assert test_prime_miller_rabin(3)
    assert not test_prime_miller_rabin(4)
    assert not test_prime_miller_rabin(111)
    assert not test_prime_miller_rabin(111111)
    assert not test_prime_miller_rabin(99999999999999999999999999)
    assert not test_prime_miller_rabin(99999999999999999999999998)
    # https://oeis.org/wiki/Higher-order_prime_numbers
    assert test_prime_miller_rabin(12055296811267)
    assert test_prime_miller_rabin(17461204521323)
    assert test_prime_miller_rabin(28871271685163)
    assert test_prime_miller_rabin(53982894593057)
    assert test_prime_miller_rabin(2**16+1)

    assert generate_prime_number(2, 5) in (2, 3, 5)

    prk, puk = generate_key_pair(11, 41, 7)
    assert encrypt(4, puk) == 148


if __name__ == "__main__":
    run_tests()

    p, q, p1, q1 = sorted([generate_prime_number(2**256, 2**512) for _ in range(4)])
    private_key_a, public_key_a = generate_key_pair(p, q)
    private_key_b, public_key_b = generate_key_pair(p1, q1)

    m = randint(1, p*q-1)
    print(f"Згенеровано повідомлення M={m}", end="\n\n")

    m_encrypted_by_a = encrypt(m, public_key_b)  # A шифрує за відкритим ключем B
    print(f"A зашифрував повідомлення відкритим ключем B, і отримав C={m_encrypted_by_a}")
    print(f"B розшифрував повідомлення своїм закритим ключем і отримав M={decrypt(m_encrypted_by_a, private_key_b)}")

    m_encrypted_by_b = encrypt(m, public_key_a)  # B, навпаки, шифрує за відкритим ключем A
    print(f"B зашифрував повідомлення відкритим ключем A, і отримав C={m_encrypted_by_b}")
    print(f"A розшифрував повідомлення своїм закритим ключем і отримав M={decrypt(m_encrypted_by_b, private_key_a)}")

    print()

    m_signed_by_a = sign(m, private_key_a)
    print(f"A підписав повідомлення, і отримав S={m_signed_by_a[1]}")
    print(f"B перевірив підпис з результатом {verify(m_signed_by_a, public_key_a)}")

    m_signed_by_b = sign(m, private_key_b)
    print(f"B підписав повідомлення, і отримав S={m_signed_by_b[1]}")
    print(f"A перевірив підпис з результатом {verify(m_signed_by_b, public_key_b)}")

    print()

    k = randint(1, p*q-1)
    print(f"A згенерував певний ключ k={k}")
    key_message = send_key(k, private_key_a, public_key_b)
    print(f"А зформував повідомлення (k1, S1)={key_message}")
    key = receive_key(key_message, private_key_b, public_key_a)
    print(f"B отримав повідомлення, після чого знайшов і перевірив ключ k={key}")

