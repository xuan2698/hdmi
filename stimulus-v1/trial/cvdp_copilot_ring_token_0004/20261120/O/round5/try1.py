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
        else:
            rst = 0
            phase = (i - 3) % 40
            if phase < 10:
                has_data_to_send = 1
                data_in = (i * 3 + 1) & 0xF
            elif phase < 20:
                has_data_to_send = 0
                data_in = (i * 5 + 2) & 0xF
            elif phase < 30:
                has_data_to_send = 1
                data_in = rng.randrange(16)
            else:
                has_data_to_send = rng.randrange(2)
                data_in = rng.randrange(16)
        row = {
            "rst": rst & 0x1,
            "data_in": data_in & 0xF,
            "has_data_to_send": has_data_to_send & 0x1,
        }
        if rng.random() < 0.3:
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
