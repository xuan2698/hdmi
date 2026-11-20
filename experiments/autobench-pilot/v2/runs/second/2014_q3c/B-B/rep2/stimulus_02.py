def Y0(x, y):
    y2 = (y >> 2) & 1
    y1 = (y >> 1) & 1
    y0 = y & 1
    return (not x and not y2 and not y1 and y0) or (not x and y2) or (x and not y2 and y1 and not y0)

def z(x, y):
    y2 = (y >> 2) & 1
    y1 = (y >> 1) & 1
    y0 = y & 1
    return (not x and not y2 and y1 and y0) or (x and y2)

def stimulus(rng, cycles):
    seq = []
    states = [0, 1, 2, 3, 4]
    for i in range(cycles):
        if i < 10:
            y = states[i % len(states)]
            x = i % 2
        elif i < 20:
            y = rng.choice(states)
            x = rng.getrandbits(1)
        else:
            y = rng.randrange(8)
            x = rng.getrandbits(1)
        seq.append({'x': x, 'y': y})
    return seq
