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
        elif i == 2:
            rst = 0
            data_in = 8
            has_data_to_send = 1
        elif i == 3:
            rst = 0
            data_in = 4
            has_data_to_send = 1
        elif i == 4:
            rst = 0
            data_in = 12
            has_data_to_send = 1
        elif i == 5:
            rst = 0
            data_in = 2
            has_data_to_send = 1
        elif i == 6:
            rst = 0
            data_in = 15
            has_data_to_send = 1
        elif i == 7:
            rst = 0
            data_in = 1
            has_data_to_send = 0
        elif i == 8:
            rst = 0
            data_in = 9
            has_data_to_send = 1
        elif i == 9:
            rst = 0
            data_in = 6
            has_data_to_send = 1
        elif i == 10:
            rst = 0
            data_in = 3
            has_data_to_send = 0
        elif i == 11:
            rst = 0
            data_in = 11
            has_data_to_send = 1
        elif i == 12:
            rst = 0
            data_in = 5
            has_data_to_send = 1
        elif i == 13:
            rst = 0
            data_in = 14
            has_data_to_send = 1
        elif i == 14:
            rst = 0
            data_in = 7
            has_data_to_send = 0
        elif i == 15:
            rst = 0
            data_in = 10
            has_data_to_send = 1
        else:
            rst = 0
            if rng.random() < 0.40:
                data_in = rng.randrange(16)
            if rng.random() < 0.35:
                has_data_to_send = rng.randrange(2)
        rows.append({
            'rst': rst & 0x1,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data_to_send & 0x1,
        })
    return rows
