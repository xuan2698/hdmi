def stimulus(rng, cycles):
    rows = []
    seq = [1, 1, 0, 1]
    for i in range(cycles):
        r = {"reset": 0, "data": 0}
        if i < 8:
            r["reset"] = 1 if i in (0, 4) else 0
            r["data"] = rng.getrandbits(1)
        elif i < 24:
            r["data"] = seq[(i - 8) % 4]
            if i == 20:
                r["reset"] = 1
        elif i < 40:
            r["data"] = rng.choice([0, 1, 1, 0, 1])
        elif i < 56:
            r["data"] = rng.getrandbits(1)
            if rng.random() < 0.3:
                r["mid"] = {"data": rng.getrandbits(1)}
        elif i < 72:
            r["data"] = seq[i % 4]
            if rng.random() < 0.2:
                r["mid"] = {"reset": 1}
        else:
            r["data"] = rng.getrandbits(1)
            if rng.random() < 0.1:
                r["reset"] = 1
        rows.append(r)
    return rows
