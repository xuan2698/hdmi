def stimulus(rng, cycles):
    rows = []
    rst = 1
    data_in = 0
    has_data_to_send = 0
    for i in range(cycles):
        if i < 2:
            rst = 1
            data_in = 0
            has_data_to_send = 0
        else:
            rst = 0
            if i == 2:
                data_in = 8
                has_data_to_send = 1
            elif i == 3:
                data_in = 4
                has_data_to_send = 1
            elif i == 4:
                data_in = 12
                has_data_to_send = 1
            elif i == 5:
                data_in = 2
                has_data_to_send = 1
            elif i < 20:
                data_in = (data_in + 3) & 0xF
                has_data_to_send = 1
            else:
                r = rng.random()
                if r < 0.45:
                    data_in = rng.randrange(16)
                if rng.random() < 0.5:
                    has_data_to_send = rng.randrange(2)
        row = {
            'rst': rst,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data_to_send & 0x1,
        }
        if i >= 2 and rng.random() < 0.25:
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
