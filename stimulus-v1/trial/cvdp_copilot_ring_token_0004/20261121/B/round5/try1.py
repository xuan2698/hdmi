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
            phase = (i - 6) % 32
            if phase < 4:
                has_data_to_send = 1
                data_in = rng.randrange(16)
            elif phase < 8:
                has_data_to_send = 0
                data_in = rng.randrange(16)
            elif phase < 12:
                has_data_to_send = 1
                data_in = 15
            elif phase < 16:
                has_data_to_send = 1
                data_in = 0
            elif phase < 20:
                has_data_to_send = 0
                data_in = 0
            elif phase < 24:
                has_data_to_send = 1
                data_in = 1 << (phase % 4)
            elif phase < 28:
                has_data_to_send = 1
                data_in = rng.randrange(16)
            else:
                has_data_to_send = 0
                data_in = 15
        row = {
            'rst': rst & 0x1,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data_to_send & 0x1,
        }
        rows.append(row)
    return rows
