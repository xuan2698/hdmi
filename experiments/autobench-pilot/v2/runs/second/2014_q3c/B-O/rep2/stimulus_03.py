def Y0(x, y):
    y2 = (y >> 2) & 1
    y1 = (y >> 1) & 1
    y0 = y & 1
    if y2 == 0 and y1 == 0 and y0 == 0:
        return x & 1
    if y2 == 0 and y1 == 0 and y0 == 1:
        return 0
    if y2 == 0 and y1 == 1 and y0 == 0:
        return x & 1
    if y2 == 0 and y1 == 1 and y0 == 1:
        return 1
    if y2 == 1 and y1 == 0 and y0 == 0:
        return 1
    return 0

def z(x, y):
    y2 = (y >> 2) & 1
    y1 = (y >> 1) & 1
    y0 = y & 1
    if y2 == 0 and y1 == 1 and y0 == 1:
        return 1
    if y2 == 1 and y1 == 0 and y0 == 0:
        return 1
    return 0

def stimulus(rng, cycles):
    seq = []
    y = 0
    for i in range(cycles):
        if i % 7 == 0:
            y = 0
        x = rng.getrandbits(1)
        seq.append({'x': x, 'y': y})
        nxt = 0
        if y == 0:
            nxt = 1 if x else 0
        elif y == 1:
            nxt = 4 if x else 1
        elif y == 2:
            nxt = 1 if x else 2
        elif y == 3:
            nxt = 2 if x else 1
        elif y == 4:
            nxt = 4 if x else 3
        y = nxt
    return seq
