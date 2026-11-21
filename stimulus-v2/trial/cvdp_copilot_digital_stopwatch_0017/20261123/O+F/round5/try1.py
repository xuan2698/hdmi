def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i < 2:
            reset = 1
            start_stop = 0
        elif i == 2:
            reset = 0
            start_stop = 0
        elif i == 3:
            start_stop = 1
        elif i == 10:
            start_stop = 0
        elif i == 11:
            start_stop = 1
        elif i == 50:
            start_stop = 0
        elif i == 51:
            start_stop = 1
        elif i == 200:
            reset = 1
        elif i == 201:
            reset = 0
            start_stop = 0
        elif i == 202:
            start_stop = 1
        elif i == 600:
            start_stop = 0
        elif i == 601:
            start_stop = 1
        elif i == 1500:
            reset = 1
        elif i == 1501:
            reset = 0
            start_stop = 1
        elif i == 2500:
            start_stop = 0
        elif i == 2501:
            start_stop = 1
        elif i == 3500:
            reset = 1
        elif i == 3501:
            reset = 0
            start_stop = 0
        elif i == 3502:
            start_stop = 1
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows
