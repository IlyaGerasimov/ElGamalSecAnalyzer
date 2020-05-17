import math

def f(x, a, h, n, dega, degh):
    if x <= n / 3:
        return (x * h) % n, dega, degh + 1
    elif x <= 2 * n/3:
        return (x ** 2) % n, 2 * dega, 2 * degh
    else:
        return (a * x) % n, dega + 1, degh


def v_2(i):
    j = 0
    while i % 2 > 0:
        i = i // 2
        j += 1
    return j


def reverse(a, b):
    n = b
    res = 1
    prev = 0
    i = 0
    while a != 1:
        temp = res
        res = res * (b // a) + prev
        prev = temp
        a_1 = b % a
        b = a
        a = a_1
        i += 1
    return res if i % 2 == 0 else -res + n


def po_pollard(a, h, n):
    T = {0: {"h": h, "dega": 0, "degh": 1}}
    h_first = h
    dega = 0
    degh = 1
    for i in range(1, n):
        #print(T)
        h, dega, degh = f(h, a, h_first, n, dega, degh)
        T_curr = dict(T)
        for k in T_curr:
            #print(T)
            if T[k]["h"] == h:
                dx = (dega - T[k]["dega"]) % n
                dy = (T[k]["degh"] - degh) % n
                if dy == 0:
                    return "Cannot solve DLOG."
                d = math.gcd(dy, n)
                if d > 1:
                    return "Cannot solve DLOG but found p factor: {}.".format(d)
                invdy = reverse(dy, n)
                return (dx * invdy) % n
            T[v_2(i)] = {"h": h, "dega": dega, "degh": degh}


'''print(po_pollard(2, 3, 11))
res = po_pollard(15, (15**4)%31, 31)

if res == 0:
    print("Cannot solve DLOG.")'''