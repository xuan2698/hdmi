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
                has_data_to_send = rng.randrange(2)
            else:
                r = rng.random()
                if r < 0.35:
                    data_in = rng.randrange(16)
                if rng.random() < 0.4:
                    has_data_to_send = rng.randrange(2)
        row = {
            'rst': rst,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data_to_send & 0x1,
        }
        if rng.random() < 0.3:
            mid = {}
            if rng.random() < 0.5:
                mid['data_in'] = rng.randrange(16)
            if rng.random() < 0.5:
                mid['has_data_to_send'] = rng.randrange(2)
            if mid:
                row['mid'] = mid
                if 'data_in' in mid:
                    data_in = mid['data_in']
                if 'has_data_to_send' in mid:
                    has_data_to_send = mid['has_data_to_send']
        rows.append(row)
    return rows
