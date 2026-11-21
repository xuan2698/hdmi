def stimulus(rng, cycles):
    rows = []
    state = {"rst": 1, "data_in": 0, "has_data_to_send": 0}
    # Reset phase
    for i in range(4):
        rows.append({"rst": 1, "data_in": 0, "has_data_to_send": 0})
    # Release reset
    rows.append({"rst": 0, "data_in": 0, "has_data_to_send": 0})
    # Build stimulus with runs
    while len(rows) < 4000:
        mode = rng.randrange(6)
        if mode == 0:
            # idle run
            n = rng.randrange(1, 8)
            for _ in range(n):
                if len(rows) >= 4000: break
                rows.append({"rst": 0, "data_in": 0, "has_data_to_send": 0})
        elif mode == 1:
            # send data run
            n = rng.randrange(1, 10)
            for _ in range(n):
                if len(rows) >= 4000: break
                rows.append({"rst": 0, "data_in": rng.randrange(16), "has_data_to_send": 1})
        elif mode == 2:
            # data but no send
            n = rng.randrange(1, 6)
            for _ in range(n):
                if len(rows) >= 4000: break
                rows.append({"rst": 0, "data_in": rng.randrange(16), "has_data_to_send": 0})
        elif mode == 3:
            # alternating
            n = rng.randrange(2, 8)
            for j in range(n):
                if len(rows) >= 4000: break
                rows.append({"rst": 0, "data_in": rng.randrange(16), "has_data_to_send": j & 1})
        elif mode == 4:
            # random burst
            n = rng.randrange(1, 6)
            for _ in range(n):
                if len(rows) >= 4000: break
                rows.append({"rst": 0, "data_in": rng.randrange(16), "has_data_to_send": rng.randrange(2)})
        else:
            # brief reset pulse
            n = rng.randrange(1, 3)
            for _ in range(n):
                if len(rows) >= 4000: break
                rows.append({"rst": 1, "data_in": 0, "has_data_to_send": 0})
            if len(rows) < 4000:
                rows.append({"rst": 0, "data_in": rng.randrange(16), "has_data_to_send": rng.randrange(2)})
    return rows[:4000]
