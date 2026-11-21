def stimulus(rng, cycles):
    rows = []
    rows.append({"reset": 1})
    rows.append({"reset": 0})
    for i in range(10):
        rows.append({"reset": 0})
    rows.append({"reset": 1})
    rows.append({"reset": 0})
    rows.append({"reset": 0, "mid": {"reset": 1}})
    rows.append({"reset": 0})
    rows.append({"reset": 1, "mid": {"reset": 0}})
    rows.append({"reset": 0})
    while len(rows) < cycles:
        r = rng.randrange(2)
        if rng.random() < 0.3:
            rows.append({"reset": r, "mid": {"reset": rng.randrange(2)}})
        else:
            rows.append({"reset": r})
    return rows[:cycles]
