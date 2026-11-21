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
            if i < 8:
                has_data_to_send = 1
                data_in = (i * 5 + 3) & 0xF
            elif i < 16:
                has_data_to_send = 0
                data_in = rng.randrange(16)
            elif i < 32:
                has_data_to_send = 1
                data_in = rng.randrange(16)
            elif i < 48:
                has_data_to_send = 0
                data_in = 0
            else:
                r = rng.random()
                if r < 0.15:
                    has_data_to_send = 0
                    data_in = rng.randrange(16)
                elif r < 0.65:
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
