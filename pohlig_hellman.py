import math
import random


def is_prime(p, k):
    if p%2 == 0 or p%3 == 0 or p%5 == 0 or p%7 == 0 or p%11 == 0:
        return False
    p_1 = p - 1
    s = 0
    t = 0
    while p_1 % 2 == 0:
        s += 1
        p_1 = p_1 // 2
    t = p_1
    a_set = set()
    for i in range(k):
        a = random.randint(2, p - 2)
        while a in a_set:
            a = random.randint(2, p - 2)
        a_set.add(a)
        if not miller_rabin(p, t, s, a):
            return False
    return True


def miller_rabin(p, t, s, a):
    x = pow(a, t, p)
    if x == 1 or x == p-1:
        return True
    for i in range(s-1):
        x = x*x % p
        if x == 1:
            return False
        elif x == p-1:
            return True
        return False


def calculate_b_primes(b):
    prime_set = [True] * (b // 2)
    for i in range(3, int(b ** 0.5) + 1, 2):
        if prime_set[i // 2]:
            prime_set[i // 2 + i::i] = [False] * len(prime_set[i // 2 + i::i])
    return [2 * i + 1 for i in range(1, b // 2) if prime_set[i]]


def factorize(n):
    factor = dict({2: 0})
    while n % 2 == 0:
        factor[2] += 1
        n = n // 2
    if n == 1:
        return factor
    if math.log(n, 2) < 30:
        p_set = calculate_b_primes(n + 1)
    else:
        p_set = calculate_b_primes(2**30)
    for prime in p_set:
        if n % prime == 0:
            factor[prime] = 1
            n = n // prime
            while n % prime == 0:
                factor[prime] += 1
                n = n // prime
        if n == 1:
            break
    if n != 1:
        exit("Can not factorize")
    return factor


def reverse(a, b):
    n = b
    res = 1
    prev = 0
    i = 0
    while a != 1:
        temp = res
        res = res * (b // a) + prev
        prev = temp
        a_1 = b%a
        b = a
        a = a_1
        i += 1
    return res if i % 2 == 0 else -res+n


def log2(a, h, t, p):
    mod = pow(2, t)
    a = a
    h = h
    b = 1 if pow(h, (p - 1) // 2, p) != 1 else 0
    log_2 = b
    h = (h * pow(a, (-b) % (p - 1), p)) % p
    for i in range(1, t):
        b = 1 if pow(h, (p - 1) // pow(2, i + 1), p) != 1 else 0
        log_2 += (pow(2, i) * b) % mod
        h = (h * pow(a, (-pow(2, i, p - 1) * b) % (p - 1), p)) % p
    return log_2


def logp(a, h, q, t, p):
    mod = pow(q, t)
    a = a
    h = h
    #print(a, h, q, t, mod)
    table = dict()
    for i in range(p):
        #print(pow(a, p // q * i, p))
        table[pow(a, p // q * i, p)] = i
    #print(table)
    c = table[pow(h, p // q, p)]
    log_p = c
    h = (h * pow(a, (-c) % (p - 1), p)) % p
    for i in range(1, t):
        c = table[pow(h, p // pow(q, i + 1, p - 1), p)]
        log_p += (pow(p, i, mod) * c) % mod
        h = (h * pow(a, (-pow(p, i) * c) % p - 1, p)) % p
    return log_p


def crt(a, factor, p):
    x = 0
    for key, value in factor.items():
        a_i = pow(key, value)
        m = (p - 1) // a_i
        m_1 = reverse(m % a_i, a_i)
        x += (a[key] * m * m_1) % (p - 1)
    return x


def pohlig_hellman(a, h, p):
    factor = factorize(p - 1)
    #print(factor)
    log = dict()
    for key, value in factor.items():
        if key == 2:
            log[2] = log2(a, h, factor[2], p)
            #print("log2", log[2])
        else:
            log[key] = logp(a, h, key, value, p)
    #print(log)
    res = crt(log, factor, p)
    return res


def weak_pohlig_hellman():
    p_ferma = random.choice([3, 5, 17, 257, 65537])
    p_mersenne_step = random.choice([2, 3, 5, 7, 13, 17, 19, 31, 61, 89])
    p_mersenne = pow(2, p_mersenne_step) - 1
    p_lower = random.choice([3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101])
    i = 10
    p_single = 2 * pow(p_lower, i) + 1
    while (not is_prime(p_single, int(math.log2(p_single)))) and i <= 200:
        i += 1
        p_single = 2 * pow(p_lower, i) + 1
    if i == 201:
        p_single = None
    small_max_factor = 2
    j = 0
    p_small = None
    while j <= 100:
        while math.log2(small_max_factor + 1) <= 256:
            small_max_factor *= random.choice([3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101])
            if math.log2(small_max_factor + 1) >= 200 and is_prime(small_max_factor + 1, int(math.log2(small_max_factor + 1))):
                p_small = small_max_factor + 1
                break
        if p_small:
            break
        j += 1
    return [p_ferma, p_mersenne, p_single, p_small]


'''print(pow(2, 8, 11))
print(pohlig_hellman(2, pow(2, 8, 11), 11))'''
