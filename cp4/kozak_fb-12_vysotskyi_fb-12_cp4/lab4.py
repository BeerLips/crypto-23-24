def generate_prime_number(lowest: int, highest: int) -> str:
    pass

def decimal_to_binary(a: int) -> str:
    binary_a = ""
    while a > 0:
        remainder = a % 2
        binary_a = str(remainder) + binary_a
        a //= 2
    return binary_a if binary_a else "0"


def horner_power(x: int, a: int, m: int) -> int:
    #  x^a (mod m)
    result = 1
    binary_a = decimal_to_binary(a)

    for bit in binary_a:
        result = (result * result) % m
        if bit == '1':
            result = (result * x) % m

    return result
