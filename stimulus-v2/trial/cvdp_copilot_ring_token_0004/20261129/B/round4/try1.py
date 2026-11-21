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
            if i < 10:
                data_in = rng.randrange(16)
                has_data_to_send = 1 if rng.random() < 0.5 else 0
            elif i < 60:
                data_in = rng.randrange(16)
                has_data_to_send = 1
            elif i < 120:
                data_in = rng.randrange(16)
                has_data_to_send = 0
            elif i < 200:
                data_in = rng.randrange(16)
                has_data_to_send = 1 if rng.random() < 0.75 else 0
            elif i < 260:
                data_in = 0
                has_data_to_send = 1
            elif i < 320:
                data_in = 15
                has_data_to_send = 1
            elif i < 380:
                data_in = rng.randrange(16)
                has_data_to_send = 0
            elif i < 500:
                data_in = rng.randrange(16)
                has_data_to_send = 1 if rng.random() < 0.3 else 0
            elif i < 700:
                data_in = rng.randrange(16)
                has_data_to_send = 1
            elif i < 900:
                data_in = rng.randrange(16)
                has_data_to_send = 0
            elif i < 1100:
                data_in = rng.randrange(16)
                has_data_to_send = 1 if rng.random() < 0.6 else 0
            elif i < 1400:
                data_in = rng.randrange(16)
                has_data_to_send = 1
            elif i < 1700:
                data_in = rng.randrange(16)
                has_data_to_send = 0
            elif i < 2000:
                data_in = rng.randrange(16)
                has_data_to_send = 1 if rng.random() < 0.5 else 0
            elif i < 2400:
                data_in = rng.randrange(16)
                has_data_to_send = 1
            elif i < 2800:
                data_in = rng.randrange(16)
                has_data_to_send = 0
            elif i < 3200:
                data_in = rng.randrange(16)
                has_data_to_send = 1 if rng.random() < 0.4 else 0
            elif i < 3600:
                data_in = rng.randrange(16)
                has_data_to_send = 1
            else:
                data_in = rng.randrange(16)
                has_data_to_send = 0
        row = {
            'rst': rst,
            'data_in': data_in,
            'has_data_to_send': has_data_to_send,
        }
        rows.append(row)
    return rows
