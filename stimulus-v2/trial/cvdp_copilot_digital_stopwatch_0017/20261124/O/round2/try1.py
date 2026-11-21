def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i < 3:
            reset = 1
            start_stop = 0
        elif i == 3:
            reset = 0
            start_stop = 0
        else:
            if i == 4:
                start_stop = 1
            elif i == 200:
                start_stop = 0
            elif i == 260:
                start_stop = 1
            elif i == 500:
                start_stop = 0
            elif i == 520:
                start_stop = 1
            elif i == 900:
                start_stop = 0
            elif i == 950:
                start_stop = 1
            elif i == 1500:
                start_stop = 0
            elif i == 1600:
                start_stop = 1
            elif i == 3000:
                start_stop = 0
            elif i == 3100:
                start_stop = 1
            elif i == 5000:
                start_stop = 0
            elif i == 5100:
                start_stop = 1
            elif i == 8000:
                start_stop = 0
            elif i == 8100:
                start_stop = 1
            elif i == 12000:
                start_stop = 0
            elif i == 12100:
                start_stop = 1
            elif i == 16000:
                start_stop = 0
            elif i == 16100:
                start_stop = 1
            elif i == 19000:
                start_stop = 0
            elif i == 19100:
                start_stop = 1
            else:
                if rng.random() < 0.001:
                    start_stop = 1 - start_stop
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows
