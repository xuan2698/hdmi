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
        elif i < 8:
            rst = 0
            data_in = (i * 3) & 0xF
            has_data_to_send = 1
        elif i < 12:
            rst = 0
            data_in = 0
            has_data_to_send = 0
        elif i < 20:
            rst = 0
            data_in = (i * 5 + 1) & 0xF
            has_data_to_send = 1
        elif i < 24:
            rst = 1
            data_in = 0
            has_data_to_send = 0
        elif i < 40:
            rst = 0
            data_in = rng.randrange(16)
            has_data_to_send = 1 if rng.random() < 0.7 else 0
        elif i < 60:
            rst = 0
            data_in = (i * 7) & 0xF
            has_data_to_send = 1
        elif i < 80:
            rst = 0
            data_in = 0
            has_data_to_send = 0
        elif i < 120:
            rst = 0
            data_in = rng.randrange(16)
            has_data_to_send = 1 if rng.random() < 0.3 else 0
        elif i < 200:
            rst = 0
            data_in = (i * 11 + 3) & 0xF
            has_data_to_send = 1 if (i % 3) == 0 else 0
        elif i < 400:
            rst = 0
            data_in = rng.randrange(16)
            has_data_to_send = 1 if rng.random() < 0.5 else 0
        elif i < 800:
            rst = 0
            data_in = (i * 13) & 0xF
            has_data_to_send = 1 if (i % 5) < 2 else 0
        elif i < 1600:
            rst = 0
            data_in = rng.randrange(16)
            has_data_to_send = 1 if rng.random() < 0.6 else 0
        elif i < 2400:
            rst = 0
            data_in = (i * 17 + 7) & 0xF
            has_data_to_send = 1 if (i % 7) < 3 else 0
        elif i < 3200:
            rst = 0
            data_in = rng.randrange(16)
            has_data_to_send = 1 if rng.random() < 0.4 else 0
        elif i < 3600:
            rst = 0
            data_in = (i * 19) & 0xF
            has_data_to_send = 1
        elif i < 3900:
            rst = 0
            data_in = rng.randrange(16)
            has_data_to_send = 1 if rng.random() < 0.5 else 0
        else:
            rst = 0
            data_in = (i * 23 + 5) & 0xF
            has_data_to_send = 1 if (i % 4) == 0 else 0
        row = {
            'rst': rst,
            'data_in': data_in,
            'has_data_to_send': has_data_to_send,
        }
        rows.append(row)
    return rows
