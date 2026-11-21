def stimulus(rng, cycles):
    rows = []
    seq = [1, 1, 0, 1]
    for i in range(cycles):
        r = {"reset": 0, "data": 0}
        if i == 0:
            r["reset"] = 1
        elif i < 8:
            r["data"] = seq[(i - 1) % 4]
        elif i < 12:
            r["data"] = rng.getrandbits(1)
        elif i == 12:
            r["reset"] = 1
        elif i < 20:
            r["data"] = seq[(i - 13) % 4]
        elif i == 20:
            r["data"] = 1
            r["mid"] = {"data": 1}
        elif i == 21:
            r["data"] = 0
            r["mid"] = {"data": 1}
        elif i == 22:
            r["data"] = 1
        elif i < 28:
            r["data"] = rng.choice([0, 1])
        else:
            r["data"] = seq[(i - 28) % 4]
        rows.append(r)
    return rows[:cycles]
