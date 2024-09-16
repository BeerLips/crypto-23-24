import random

def ext_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = ext_gcd(b % a, a)
        return gcd, y - (b // a) * x, x


def millerabin_test(p, k):
    if p == 2 or p == 3: #перевірка на особливі випадки(2 і 3 - прості числа)
        return True
    if p % 2 == 0 or p < 2: #перевірка на парність
        return False
    s, d = 0, p-1
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(k):
        x = random.randint(1, p - 1)
        gcd1 = pow(x, d, p)
        if gcd1 == 1 or gcd1 == p - 1:
            continue

        for _ in range(1, s):
            gcd1 = pow(gcd1, 2, p)
            if gcd1 == p - 1:
                break
        else:
            return False # p - є складеним

    return True # p - псевдопросте


def generate_prime():
    prime = random.getrandbits(256)
    if prime % 2 == 0:
        prime += 1
    while not millerabin_test(prime, 30):
        prime += 2

    return prime

def GenerateNumPair():
    p, q, p1, q1 = 0, 0, 0, 0
    while True:
        p = generate_prime()
        q = generate_prime()
        p1 = generate_prime()
        q1 = generate_prime()
        if p*q <= p1*q1:
            break
    return p, q, p1, q1




def RSA_Keys(p, q):
    n = p*q
    fo = (p-1)*(q-1) #функція Ойлера
    while True:
        e = random.randint(2, fo-1)
        if ext_gcd(e, fo)[0] == 1:
            d = modInverse(e, fo)
            break

    return (e, n), (d, p, q)

def modInverse(num, mod):
    a, b = num, mod
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = divmod(b, a)
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    return x % mod


def Encrypt(message, e, n):
    encrypted_message = pow(message, e, n)
    return encrypted_message


def Decrypt(encrypted_message, d, p, q):
    decrypted_message = pow(encrypted_message, d, p*q)
    return decrypted_message


def Sign(message, secret_key):
    sign = pow(message, secret_key[0], secret_key[1]*secret_key[2])
    return sign


def Verify(signed_message, sign, public_key):
    return signed_message == pow(sign, public_key[0], public_key[1])
    

def SendKey(k, secret_key, public_key_B):
    k1 = Encrypt(k, public_key_B[0], public_key_B[1])
    s = Sign(k, secret_key)
    s1 = Encrypt(s, public_key_B[0], public_key_B[1])
    print(f"k1: {k1} \ns: {s}\ns1: {s1}")
    return (k1, s1)


def RecieveKey(k_list, secret_key, public_key_A):
    k = Decrypt(k_list[0], secret_key[0], secret_key[1], secret_key[2])
    s = Decrypt(k_list[1], secret_key[0], secret_key[1], secret_key[2])
    sign_verification = Verify(k, s, public_key_A)
    print(f"Функція отримання ключа: ")
    print(f"k: {k} \ns: {s}\ncheck: {sign_verification}")
    return (k, sign_verification)

#Генерація пари простих чисел  
p, q, p1, q1 = GenerateNumPair()

print("p =", p)
print("q =",q)
print("p1 =",p1)
print("q1 =",q1)
print(f"===============================")
#Генерація ключів дла абонентів А та B
public_key_A, secret_key_A = RSA_Keys(p, q)
public_key_B, secret_key_B = RSA_Keys(p1, q1)

print("Відкритий ключ A (e, n):", public_key_A)
print("Секретний ключ A (d, p, q):", secret_key_A)
print("Відкритий ключ B (e, n):", public_key_B)
print("Секретний ключ B (d, p, q):", secret_key_B)
print(f"===============================")

M = random.randint(0, public_key_A[1] - 1)
print("Відкритий текст (M):", M)
C = Encrypt(M, public_key_A[0], public_key_A[1])
d_2 = secret_key_A[0]
n_2 = secret_key_A[1]
print("Шифротекст (C):", C)
M = Decrypt(C, secret_key_A[0], secret_key_A[1], secret_key_A[2])
print("Розшифрований (M) :", M)
print(f"===============================")

signed = Sign(M, secret_key_A)
print("Підпис (S):", signed)
print("Перевірка підпису:", Verify(M, signed, public_key_A))
print(f"===============================")

print(f"Функція відправки ключа: ")
k = random.randint(0, public_key_A[1])
print("k:", k)
msg = SendKey(k, secret_key_A, public_key_B)
#print(public_key_B[1] >= public_key_A[1])
print("Відправлений ключ (k1, S1):", msg)
print("Отриманий ключ (k, sign_verification):", RecieveKey(msg, secret_key_B, public_key_A))
print(f"===============================")

#Тести з сервером
###1,беремо ключ на сервері, шифруємо його тут, і розшифровуємо на сервері
print(f"Test -- Encryption")
server_key = 'AE4A23FE2E44AD45FE9867F1192F2EC4D09E578981DAAF2E451FC77E5A7A184D'
n = int(server_key, 16)
print(f"n: ", n)
public_e = '10001'
e = int(public_e, 16)
print(f"e: ", e)
M1 = int('666666',16)
public_key1_A = (e,n)
print(f"Повідомлення_1: ", M1)
encrypted_text = Encrypt(M1, e, n)
print(f"Зашифрований текст: ", hex(encrypted_text).upper()[2:])
print(f"===============================")

###2
print(f"Test -- Decryption")

def RSA_Keys_2(p, q):
    n = p*q
    fo = (p-1)*(q-1) #функція Ойлера
    while True:
        e = int('10001',16)
        if ext_gcd(e, fo)[0] == 1:
            d = modInverse(e, fo)
            break

    return (e, n), (d, p, q)
p2 = 53942798491662374014013154466993223980861401413964560391950983741994658392791
q2 = 83230260726133430091891278119226286536741447953693128832336769322857561796643
p3 = 83145974407219291949006645963343446718067013046388947315900544481589237159467
q3 = 98218213215060430385367454899289751131197639009554022820863489091984936291813

print("p2 =", p2)
print("q2 =", q2)
print("p3 =", p3)
print("q3 =", q3)

public_key2_A, secret_key2_A = RSA_Keys_2(p2, q2)
public_key2_B, secret_key2_B = RSA_Keys_2(p3, q3)
n2_hex = hex(public_key2_A[1]).upper()[2:]

print("Відкритий ключ A (hex):", (e, n2_hex))
print("Секретний ключ A (d, p, q):", secret_key2_A)
print(f"===============================")

    
C2 = int('3F0150FF1D6091793360970DE2C37EBF4EB70F239E4E0D2E3DCDCACBE9CDA0696A13746EC77BBC04CFD63DF933CC5EAD496A3EF8B51895F40CF5734C7C3D48F7',16) #шифротекст отриманий сервером
d_2 = secret_key2_A[0] 
M2 = Decrypt(C2, d_2, p2, q2)
print(f"Розшифроване повідомлення: ", hex(M2).upper()[2:])
print(f"===============================")

###3
print(f"Test -- Sign")
print("Відкритий ключ A (hex):", (e, n2_hex))
print(f"Секретний ключ А(d, p, q): ", secret_key2_A)
s3 = Sign(M1, secret_key2_A)
print(f"Підпис 2(s3): ", hex(s3).upper()[2:])

print(f"===============================")
##Беремо повідомлення з першого тесту М1, підписуємо його на сервері, та перевіряємо підпис локально
###4
print(f"Test -- Verify")
server_sign = int("1829319C6C3166C3E57F6159B23236AE46F45E94E6B2FC3E1F96F4A95282F9DC", 16)
server_sign_hex = hex(server_sign)[2:]
print(f"server_sign_hex: ", server_sign_hex)
print(Verify(M1, server_sign, public_key1_A))
print(f"===============================")

