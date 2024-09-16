import math
import random

# Функція для перевірки чи число є простим за алгоритмом Міллера-Рабіна
def is_prime(n, k=5):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True

    # Знайдемо d, таке що n = 2^r * d + 1
    d = n - 1
    while d % 2 == 0:
        d //= 2

    # Перевірка простоти за допомогою k тестів Міллера-Рабіна
    for _ in range(k):
        if not miller_rabin_test(d, n):
            return False
    return True

# Тест Міллера-Рабіна для одного свідчення
def miller_rabin_test(d, n):
    a = 2 + random.randint(1, n - 4)
    x = pow(a, d, n)

    if x == 1 or x == n - 1:
        return True

    while d != n - 1:
        x = (x * x) % n
        d *= 2

        if x == 1:
            return False
        if x == n - 1:
            return True

    return False

# Генерація випадкового простого числа заданої бітності
def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        if is_prime(num):
            print(f"Generated prime number: {num} (Bits: {bits})")
            return num

# Генерація пари публічного та приватного ключів
def generate_key_pair(bits):
    p = generate_prime(bits)
    q = generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537  # Вибір значення e (зазвичай фіксоване)
    d = pow(e, -1, phi)

    return ((n, e), (d, p, q))  # Повертаємо публічний та приватний ключі

# Шифрування повідомлення за допомогою публічного ключа
def encrypt(message, public_key):
    n, e = public_key
    return pow(message, e, n)

# Дешифрування повідомлення за допомогою приватного ключа
def decrypt(ciphertext, private_key):
    d, p, q = private_key
    return pow(ciphertext, d, p * q)

# Створення підпису за допомогою приватного ключа
def sign(message, private_key):
    d, p, q = private_key
    return pow(message, d, p * q)

# Перевірка підпису за допомогою публічного ключа
def verify(signature, message, public_key):
    n, e = public_key
    return pow(signature, e, n) == message

# Реалізація протоколу обміну ключами
def send_key(key, sender_private_key, receiver_public_key):
    encrypted_key = encrypt(key, receiver_public_key)
    signature = sign(key, sender_private_key)
    return encrypted_key, signature

def receive_key(encrypted_key, signature, receiver_private_key, sender_public_key):
    decrypted_key = decrypt(encrypted_key, receiver_private_key)
    if verify(signature, decrypted_key, sender_public_key):
        return decrypted_key
    else:
        return None

# Приклади використання функцій
# Генерація ключів для двох користувачів A та B
key_pair_A = generate_key_pair(256)
key_pair_B = generate_key_pair(256)

# Зашифроване та розшифроване повідомлення, підпис та перевірка підпису
message = random.randint(0, key_pair_B[0][0])
encrypted_message = encrypt(message, key_pair_B[0])
decrypted_message = decrypt(encrypted_message, key_pair_B[1])
signature = sign(message, key_pair_A[1])
verification_result = verify(signature, message, key_pair_A[0])

# Обмін ключами між A та B
shared_key = random.randint(0, key_pair_B[0][0])
encrypted_key, signature = send_key(shared_key, key_pair_A[1], key_pair_B[0])
received_key = receive_key(encrypted_key, signature, key_pair_B[1], key_pair_A[0])

# Генерація пар ключів для двох сутностей A та B
print("Generating key pairs for A and B...")
key_pair_A = generate_key_pair(256)
key_pair_B = generate_key_pair(256)

# Виведення публічних і приватних ключів у шістнадцятковому форматі
print(f"Entity A's Public Key: {key_pair_A[0]} (Hex: {key_pair_A[0][0]:x}, {key_pair_A[0][1]:x})")
print(f"Entity A's Private Key: {key_pair_A[1]} (Hex: {key_pair_A[1][0]:x}, {key_pair_A[1][1]:x}, {key_pair_A[1][2]:x})")
print(f"Entity B's Public Key: {key_pair_B[0]} (Hex: {key_pair_B[0][0]:x}, {key_pair_B[0][1]:x})")
print(f"Entity B's Private Key: {key_pair_B[1]} (Hex: {key_pair_B[1][0]:x}, {key_pair_B[1][1]:x}, {key_pair_B[1][2]:x})")

message = random.randint(0, key_pair_B[0][0])  # Генерація випадкового повідомлення
print(f"Original Message: {message} (Hex: {message:x})")

encrypted_message = encrypt(message, key_pair_B[0])  # Шифрування публічним ключем B
print(f"Encrypted Message: {encrypted_message} (Hex: {encrypted_message:x})")

decrypted_message = decrypt(encrypted_message, key_pair_B[1])  # Дешифрування приватним ключем B
print(f"Decrypted Message: {decrypted_message} (Hex: {decrypted_message:x})")

signature = sign(message, key_pair_A[1])  # Підпис повідомлення сутністю A
print(f"Signature: {signature} (Hex: {signature:x})")

verification_result = verify(signature, message, key_pair_A[0])  # Перевірка підпису A
print(f"Verification Result: {'Successful' if verification_result else 'Failed'}")

# Тест 1: Перевірка підпису
print("//////////////test 1 verify")
print(f"Original Message (Hex): {message:x}")
print(f"Signature (Hex): {signature:x}")
print(f"Sender Modulus (Hex): {key_pair_A[0][0]:x}")
print(f"Public Exponent (Hex): {key_pair_A[0][1]:x}")

# Тест шифрування
print("Encryption Test")
print(f"Modulus (Hex): {key_pair_B[0][0]:x}")
print(f"Public Exponent (Hex): {key_pair_B[0][1]:x}")
print(f"Message (Hex): {message:x}")

# Реалізація протоколу обміну ключами
shared_key = random.randint(0, key_pair_B[0][0])
print(f"Shared Key: {shared_key} (Hex: {shared_key:x})")

encrypted_key, signature = send_key(shared_key, key_pair_A[1], key_pair_B[0])
print(f"Encrypted Key: {encrypted_key} (Hex: {encrypted_key:x}), Signature: {signature} (Hex: {signature:x})")

received_key = receive_key(encrypted_key, signature, key_pair_B[1], key_pair_A[0])
print(f"Received Key: {received_key} (Should match Shared Key if verification is successful) (Hex: {received_key:x})")
