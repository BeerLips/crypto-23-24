from random import randint
from typing import Tuple


class PrivateKey:

    def __init__(self, d, p, q):
        self.d = d
        self.p = p
        self.q = q


class PublicKey:

    def __init__(self, n, e):
        self.n = n
        self.e = e


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

    while True:
        p = randint(lowest, highest)
        if test_prime_miller_rabin(p):
            return p


def generate_keys_from_2_prime_numbers(p: int, q: int) -> Tuple[PrivateKey, PublicKey]:
    n = p*q
    euler = (p-1)*(q-1)

    e = 2**16+1

    d = mod_inverse(e, euler)
    return PrivateKey(d, p, q), PublicKey(n, 3)


def encrypt(open_text: int, public_key: PublicKey) -> int:
    encrypted_text = horner_power(open_text, public_key.e, public_key.n)


def run_tests():
    assert distribute_number(13)[0] == 3
    assert distribute_number(13)[1] == 2
    assert distribute_number(100)[1] == 0
    print("distribute_number works fine")
    assert horner_power(10, 2, 101) == 100
    print("horner_power works fine")
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
    print("test_prime_miller_rabin works fine")
    assert generate_prime_number(2, 5) in (2, 3, 5)



if __name__ == "__main__":
    run_tests()
    p, q, p1, q1 = sorted([generate_prime_number(2**256, 2**512) for _ in range(4)])
