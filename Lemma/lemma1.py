import random

def round0(t0, p, q):
    """
    Round0: Zq → {0,1} × Zp
    """
    z0 = t0 % p
    flag0 = random.choices([0, 1], [q - 4 * abs(t0 % p) * p, 4 * abs(t0 % p) * p])[0]
    return flag0, z0

def round1(t1, p, q):
    """
    Round1: Zq → {0,1} × Z2p
    """
    z1 = t1 % p
    z1_prime = (t1 + p) % p
    flag1 = random.choices([0, 1], [q - 4 * abs(t1 % p) * p, 4 * abs(t1 % p) * p])[0]
    return flag1, z1, z1_prime

def share_conversion(x, e, p, q):
    """
    Core lemma for share conversion.
    
    Let p, q ∈ N with p | q. Then, there exist efficient procedures Round0: Zq → {0,1} × Zp 
    and Round1: Zq → {0,1} × Z2p such that the following holds:
    
    For any x ∈ Zp, any e ∈ Z with |e| < q/(4p), and any t0, t1 with
    t0 + t1 = (q/p) * x + e (mod q),
    it holds:
    
    x = z0 + z1 (mod p) if flag0 = 0 or flag1 = 0,
    x = z0 + z1' (mod p) if flag0 = flag1 = 1,
    
    where (flag0, z0) ← Round0(t0) and (flag1, z1, z1') ← Round1(t1).
    
    Further, for t0, t1 chosen at random, it holds flag0 = flag1 = 0 with probability at least 
    1 - (4 * |e| * p) / q.
    """
    assert abs(e) < q / (4 * p), "Error term e is out of bounds"
    assert q % p == 0, "p must divide q"

    t0 = random.randint(0, q - 1)
    t1 = (q * x + e - t0) % q

    flag0, z0 = round0(t0, p, q)
    flag1, z1, z1_prime = round1(t1, p, q)

    if flag0 == 0 or flag1 == 0:
        return z0, z1
    elif flag0 == 1 and flag1 == 1:
        return z0, z1_prime
    else:
        raise ValueError("Invalid flags")

p = 5
q = 25252525
x = 3
e = 2

z0, z1 = share_conversion(x, e, p, q)
print(f"z0: {z0}, z1: {z1}")
print(f"z0 + z1 = {z1 + z0}")

