def ext_euclid(a: int, b: int):
    prev_r, r = a, b
    prev_u, u = 1, 0
    prev_v, v = 0, 1

    while r:
        q = prev_r // r
        prev_r, r = r, prev_r - q * r
        prev_u, u = u, prev_u - q * u
        prev_v, v = v, prev_v - q * v

    return prev_r, prev_u, prev_v

