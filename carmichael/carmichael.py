from sympy import isprime

def iscarmichael(n):
    for a in range(2, n):
        if pow(a, n, n) != a:
            return False
    return True

def printcarmichael(lo, hi):
    if lo % 2 == 0:
        lo -= 1
    for n in range(lo, hi, 2):
        if not isprime(n):
            if iscarmichael(n):
                pass
    return

if __name__ == "__main__":
    # printcarmichael(1, 1000000)
    print(iscarmichael(825265))