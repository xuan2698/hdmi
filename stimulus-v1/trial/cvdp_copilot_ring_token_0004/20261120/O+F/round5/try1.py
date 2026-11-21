def stimulus(rng, cycles):
    rows = []
    rst = 1
    data_in = 0
    has_data_to_send = 0
    for i in range(cycles):
        if i < 3:
            rst = 1
            data_in = 0
            has_data_to_send = 0
        elif i < 6:
            rst = 0
            data_in = 0
            has_data_to_send = 0
        else:
            rst = 0
            phase = (i - 6) % 40
            if phase < 4:
                has_data_to_send = 1
                data_in = (i * 5 + 3) & 0xF
            elif phase < 8:
                has_data_to_send = 0
                data_in = rng.randrange(16)
            elif phase < 12:
                has_data_to_send = 1
                data_in = rng.randrange(16)
            elif phase < 16:
                has_data_to_send = 0
                data_in = 0
            elif phase < 20:
                has_data_to_send = 1
                data_in = (i ^ 0xA) & 0xF
            elif phase < 24:
                has_data_to_send = rng.randrange(2)
                data_in = rng.randrange(16)
            elif phase < 28:
                has_data_to_send = 1
                data_in = 0xF
            elif phase < 32:
                has_data_to_send = 0
                data_in = rng.randrange(16)
            elif phase < 36:
                has_data_to_send = 1
                data_in = (i * 7) & 0xF
            else:
                has_data_to_send = rng.randrange(2)
                data_in = rng.randrange(16)
        row = {
            "rst": rst & 0x1,
            "data_in": data_in & 0xF,
            "has_data_to_send": has_data_to_send & 0x1,
        }
        if i >= 6 and rng.random() < 0.3:
            mid_data = rng.randrange(16)
            mid_send = rng.randrange(2)
            row["mid"] = {
                "rst": rst & 0x1,
                "data_in": mid_data & 0xF,
                "has_data_to_send": mid_send & 0x1,
            }
            data_in = mid_data
            has_data_to_send = mid_send
        rows.append(row)
    return rows
