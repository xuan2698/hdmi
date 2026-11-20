def stimulus(rng, cycles):
    out = []
    for i in range(cycles):
        if i == 0:
            out.append({'areset': 1, 'x': 0})
        elif i == 1:
            out.append({'areset': 0, 'x': 0})
        elif i == 2:
            out.append({'areset': 0, 'x': 1})
        elif i == 3:
            out.append({'areset': 0, 'x': 0})
        elif i == 4:
            out.append({'areset': 0, 'x': 1})
        elif i == 5:
            out.append({'areset': 0, 'x': 1})
        elif i == 6:
            out.append({'areset': 0, 'x': 0})
        elif i == 7:
            out.append({'areset': 0, 'x': 0})
        elif i == 8:
            out.append({'areset': 1, 'x': 1})
        elif i == 9:
            out.append({'areset': 0, 'x': 1})
        elif i == 10:
            out.append({'areset': 0, 'x': 0})
        elif i == 11:
            out.append({'areset': 0, 'x': 1})
        elif i == 12:
            out.append({'areset': 0, 'x': 0})
        elif i == 13:
            out.append({'areset': 0, 'x': 1})
        elif i == 14:
            out.append({'areset': 0, 'x': 1})
        elif i == 15:
            out.append({'areset': 0, 'x': 1})
        elif i == 16:
            out.append({'areset': 0, 'x': 0})
        elif i == 17:
            out.append({'areset': 0, 'x': 0})
        elif i == 18:
            out.append({'areset': 0, 'x': 0})
        elif i == 19:
            out.append({'areset': 1, 'x': 0})
        else:
            r = rng.random()
            if r < 0.05:
                out.append({'areset': 1, 'x': rng.getrandbits(1)})
            else:
                out.append({'areset': 0, 'x': rng.getrandbits(1)})
    return out
