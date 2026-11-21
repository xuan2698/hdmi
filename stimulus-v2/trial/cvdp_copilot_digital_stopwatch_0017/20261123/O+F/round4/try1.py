def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i == 0:
            reset = 1
            start_stop = 0
        elif i == 1:
            reset = 1
            start_stop = 0
        elif i == 2:
            reset = 0
            start_stop = 0
        elif i == 3:
            reset = 0
            start_stop = 1
        elif i == 4:
            reset = 0
            start_stop = 1
        elif i == 5:
            reset = 0
            start_stop = 0
        elif i == 6:
            reset = 0
            start_stop = 1
        elif i == 7:
            reset = 0
            start_stop = 1
        elif i == 8:
            reset = 0
            start_stop = 0
        elif i == 9:
            reset = 0
            start_stop = 1
        elif i == 20:
            start_stop = 0
        elif i == 21:
            start_stop = 1
        elif i == 40:
            start_stop = 0
        elif i == 41:
            start_stop = 1
        elif i == 100:
            reset = 1
        elif i == 101:
            reset = 1
        elif i == 102:
            reset = 0
            start_stop = 0
        elif i == 103:
            start_stop = 1
        elif i == 200:
            start_stop = 0
        elif i == 201:
            start_stop = 1
        elif i == 500:
            reset = 1
        elif i == 501:
            reset = 1
        elif i == 502:
            reset = 0
            start_stop = 0
        elif i == 503:
            start_stop = 1
        elif i == 1000:
            start_stop = 0
        elif i == 1001:
            start_stop = 1
        elif i == 2000:
            reset = 1
        elif i == 2001:
            reset = 1
        elif i == 2002:
            reset = 0
            start_stop = 1
        elif i == 3000:
            start_stop = 0
        elif i == 3001:
            start_stop = 1
        elif i == 3900:
            reset = 1
        elif i == 3901:
            reset = 1
        elif i == 3902:
            reset = 0
            start_stop = 0
        elif i == 3903:
            start_stop = 1
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows
