from calc import pow


def table(a, n, t):
    l = list()
    a = pow(a, t, n)
    for q in range(1, int(n / t) + 2):
        l.append(pow(a, q, n))
    return l

def big_little(a, h, n, t):
    l = table(a, n, t)
    el = h
    for r in range(1, t + 1):
        el = el * a
        if el in l:
            q = l.index(el) + 1
            return q * t - r
    return None

