def stimulus(rng, cycles):
    out = []
    seq = [1, 1, 0, 1]
    i = 0
    for c in range(cycles):
        if c == 0:
            reset = 1
            data = rng.getrandbits(1)
        elif c < 4:
            reset = 0
            data = rng.getrandbits(1)
        elif c % 17 == 0:
            reset = 1
            data = rng.getrandbits(1)
        elif c % 17 == 1:
            reset = 0
            data = rng.getrandbits(1)
        elif c % 13 == 0:
            reset = 0
            data = seq[i % 4]
            i += 1
        elif c % 7 == 0:
            reset = 0
            data = 1
        elif c % 7 == 1:
            reset = 0
            data = 1
        elif c % 7 == 2:
            reset = 0
            data = 0
        elif c % 7 == 3:
            reset = 0
            data = 1
        else:
            reset = 0
            data = rng.getrandbits(1)
        out.append({'reset': reset, 'data': data})
    return out
