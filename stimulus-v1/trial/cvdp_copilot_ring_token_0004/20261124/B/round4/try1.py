def stimulus(rng, cycles):
    rows = []
    for _ in range(4):
        rows.append({"rst": 1, "data_in": 0, "has_data_to_send": 0})
    rows.append({"rst": 0, "data_in": 0, "has_data_to_send": 0})
    while len(rows) < 4000:
        mode = rng.randrange(12)
        if mode == 0:
            n = rng.randrange(1, 6)
            for _ in range(n):
                if len(rows) >= 4000: break
                rows.append({"rst": 0, "data_in": 0, "has_data_to_send": 0})
        elif mode == 1:
            n = rng.randrange(1, 9)
            for _ in range(n):
                if len(rows) >= 4000: break
                rows.append({"rst": 0, "data_in": rng.randrange(16), "has_data_to_send": 1})
        elif mode == 2:
            n = rng.randrange(1, 5)
            for _ in range(n):
                if len(rows) >= 4000: break
                rows.append({"rst": 0, "data_in": rng.randrange(16), "has_data_to_send": 0})
        elif mode == 3:
            n = rng.randrange(2, 10)
            for j in range(n):
                if len(rows) >= 4000: break
                rows.append({"rst": 0, "data_in": rng.randrange(16), "has_data_to_send": j & 1})
        elif mode == 4:
            n = rng.randrange(1, 5)
            for _ in range(n):
                if len(rows) >= 4000: break
                rows.append({"rst": 0, "data_in": rng.randrange(16), "has_data_to_send": rng.randrange(2)})
        elif mode == 5:
            n = rng.randrange(1, 3)
            for _ in range(n):
                if len(rows) >= 4000: break
                rows.append({"rst": 1, "data_in": 0, "has_data_to_send": 0})
            if len(rows) < 4000:
                rows.append({"rst": 0, "data_in": rng.randrange(16), "has_data_to_send": rng.randrange(2)})
        elif mode == 6:
            n = rng.randrange(4, 12)
            for _ in range(n):
                if len(rows) >= 4000: break
                rows.append({"rst": 0, "data_in": rng.randrange(16), "has_data_to_send": 1})
        elif mode == 7:
            n = rng.randrange(1, 4)
            for _ in range(n):
                if len(rows) >= 4000: break
                rows.append({"rst": 0, "data_in": 0, "has_data_to_send": 1})
        elif mode == 8:
            n = rng.randrange(4, 9)
            for j in range(n):
                if len(rows) >= 4000: break
                rows.append({"rst": 0, "data_in": (j * 3 + rng.randrange(4)) & 15, "has_data_to_send": 1})
        elif mode == 9:
            n = rng.randrange(2, 7)
            for j in range(n):
                if len(rows) >= 4000: break
                rows.append({"rst": 0, "data_in": rng.randrange(16), "has_data_to_send": 1 if (j % 3) == 0 else 0})
        elif mode == 10:
            n = rng.randrange(4, 9)
            for j in range(n):
                if len(rows) >= 4000: break
                rows.append({"rst": 0, "data_in": (j * 5 + 1) & 15, "has_data_to_send": 1})
        else:
            n = rng.randrange(3, 8)
            for j in range(n):
                if len(rows) >= 4000: break
                rows.append({"rst": 0, "data_in": rng.randrange(16), "has_data_to_send": 1 if (j & 1) == 0 else 0})
    return rows[:4000]
