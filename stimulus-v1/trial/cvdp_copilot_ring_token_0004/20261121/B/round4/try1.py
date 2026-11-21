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
        elif i < 8:
            rst = 0
            data_in = 0
            has_data_to_send = 0
        else:
            rst = 0
            phase = (i - 8) % 24
            if phase == 0:
                has_data_to_send = 1
                data_in = rng.randrange(16)
            elif phase == 1:
                has_data_to_send = 1
                data_in = rng.randrange(16)
            elif phase == 2:
                has_data_to_send = 1
                data_in = 15
            elif phase == 3:
                has_data_to_send = 0
                data_in = rng.randrange(16)
            elif phase == 4:
                has_data_to_send = 1
                data_in = 0
            elif phase == 5:
                has_data_to_send = 0
                data_in = 15
            elif phase == 6:
                has_data_to_send = 1
                data_in = rng.randrange(16)
            elif phase == 7:
                has_data_to_send = 1
                data_in = rng.randrange(16)
            elif phase == 8:
                has_data_to_send = 0
                data_in = 0
            elif phase == 9:
                has_data_to_send = 1
                data_in = 1
            elif phase == 10:
                has_data_to_send = 1
                data_in = 2
            elif phase == 11:
                has_data_to_send = 1
                data_in = 4
            elif phase == 12:
                has_data_to_send = 1
                data_in = 8
            elif phase == 13:
                has_data_to_send = 0
                data_in = rng.randrange(16)
            elif phase == 14:
                has_data_to_send = 1
                data_in = rng.randrange(16)
            elif phase == 15:
                has_data_to_send = 1
                data_in = 15
            elif phase == 16:
                has_data_to_send = 0
                data_in = 0
            elif phase == 17:
                has_data_to_send = 1
                data_in = rng.randrange(16)
            elif phase == 18:
                has_data_to_send = 0
                data_in = rng.randrange(16)
            elif phase == 19:
                has_data_to_send = 1
                data_in = 0
            elif phase == 20:
                has_data_to_send = 1
                data_in = rng.randrange(16)
            elif phase == 21:
                has_data_to_send = 0
                data_in = 15
            elif phase == 22:
                has_data_to_send = 1
                data_in = rng.randrange(16)
            else:
                has_data_to_send = 0
                data_in = 0
        row = {
            'rst': rst & 0x1,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data_to_send & 0x1,
        }
        rows.append(row)
    return rows
