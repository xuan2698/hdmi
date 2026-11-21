def stimulus(rng, cycles):
    rows = []
    rst = 1
    data_in = 0
    has_data_to_send = 0
    for i in range(cycles):
        if i < 4:
            rst = 1
            data_in = 0
            has_data_to_send = 0
        else:
            rst = 0
            if i < 12:
                has_data_to_send = 1
                data_in = (i * 3 + 1) & 0xF
            elif i < 20:
                has_data_to_send = 0
                data_in = rng.randrange(16)
            elif i < 40:
                has_data_to_send = 1
                data_in = rng.randrange(16)
            else:
                r = rng.random()
                if r < 0.2:
                    has_data_to_send = 0
                    data_in = rng.randrange(16)
                elif r < 0.7:
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
        if rng.random() < 0.25:
            mid = {
                "rst": rst & 0x1,
                "data_in": rng.randrange(16),
                "has_data_to_send": rng.randrange(2),
            }
            row["mid"] = mid
            data_in = mid["data_in"]
            has_data_to_send = mid["has_data_to_send"]
        rows.append(row)
    return rows
