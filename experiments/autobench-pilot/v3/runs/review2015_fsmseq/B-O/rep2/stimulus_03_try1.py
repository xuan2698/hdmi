def stimulus(rng, cycles):
    rows = []
    seq = [1, 1, 0, 1]
    for i in range(cycles):
        r = {"reset": 0, "data": 0}
        if i < 16:
            if i < 4:
                r["data"] = seq[i]
            elif i == 4:
                r["reset"] = 1
            elif i < 9:
                r["data"] = seq[i - 5]
            elif i == 9:
                r["data"] = 1
                r["mid"] = {"data": 1}
            elif i == 10:
                r["data"] = 0
                r["mid"] = {"data": 1}
            elif i == 11:
                r["data"] = 1
            elif i == 12:
                r["reset"] = 1
                r["mid"] = {"reset": 0}
            elif i == 13:
                r["data"] = 1
            elif i == 14:
                r["data"] = 1
                r["mid"] = {"data": 0}
            else:
                r["data"] = 1
        else:
            r["reset"] = 1 if rng.randrange(20) == 0 else 0
            r["data"] = rng.getrandbits(1)
            if rng.randrange(4) == 0:
                r["mid"] = {"data": rng.getrandbits(1)}
        rows.append(r)
    return rows
