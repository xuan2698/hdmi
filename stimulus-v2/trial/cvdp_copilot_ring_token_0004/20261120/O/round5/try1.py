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
            if i == 3:
                data_in = rng.randrange(16)
                has_data_to_send = 1
            elif i < 12:
                data_in = rng.randrange(16)
                has_data_to_send = rng.randrange(2)
            else:
                r = rng.random()
                if r < 0.4:
                    data_in = rng.randrange(16)
                if rng.random() < 0.55:
                    has_data_to_send = rng.randrange(2)
                if rng.random() < 0.03:
                    rst = 1
                    data_in = 0
                    has_data_to_send = 0
        row = {
            'rst': rst & 0x1,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data_to_send & 0x1,
        }
        if rng.random() < 0.35:
            mid = {}
            if rng.random() < 0.5:
                mid['data_in'] = rng.randrange(16)
                data_in = mid['data_in']
            if rng.random() < 0.5:
                mid['has_data_to_send'] = rng.randrange(2)
                has_data_to_send = mid['has_data_to_send']
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows
