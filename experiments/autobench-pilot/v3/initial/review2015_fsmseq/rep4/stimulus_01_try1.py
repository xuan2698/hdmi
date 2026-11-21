def stimulus(rng, cycles):
    rows = []
    seq = [1, 1, 0, 1]
    for i in range(cycles):
        r = {"reset": 0, "data": 0}
        if i < 16:
            if i == 0:
                r["reset"] = 1
            elif i < 8:
                r["data"] = seq[(i - 1) % 4]
            else:
                r["data"] = rng.getrandbits(1)
        else:
            r["data"] = rng.getrandbits(1)
            if rng.randrange(10) == 0:
                r["reset"] = 1
        if rng.randrange(4) == 0:
            r["mid"] = {"data": rng.getrandbits(1)}
        rows.append(r)
    return rows
