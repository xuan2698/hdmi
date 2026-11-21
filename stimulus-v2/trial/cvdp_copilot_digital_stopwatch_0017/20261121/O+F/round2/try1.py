def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i == 0:
            reset = 1
            start_stop = 0
        elif i == 3:
            reset = 0
            start_stop = 0
        elif i == 5:
            reset = 0
            start_stop = 1
        elif i == 200:
            start_stop = 0
        elif i == 260:
            start_stop = 1
        elif i == 500:
            reset = 1
        elif i == 503:
            reset = 0
            start_stop = 1
        elif i == 900:
            start_stop = 0
        elif i == 950:
            start_stop = 1
        elif i == 1500:
            reset = 1
        elif i == 1502:
            reset = 0
            start_stop = 0
        elif i == 1510:
            start_stop = 1
        elif i == 3000:
            start_stop = 0
        elif i == 3100:
            start_stop = 1
        elif i == 5000:
            reset = 1
        elif i == 5002:
            reset = 0
            start_stop = 1
        elif i == 8000:
            start_stop = 0
        elif i == 8100:
            start_stop = 1
        elif i == 12000:
            reset = 1
        elif i == 12002:
            reset = 0
            start_stop = 1
        elif i == 16000:
            start_stop = 0
        elif i == 16100:
            start_stop = 1
        elif i == 19000:
            reset = 1
        elif i == 19002:
            reset = 0
            start_stop = 1
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows
