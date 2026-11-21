def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i < 3:
            reset = 1
            start_stop = 0
        elif i < 6:
            reset = 0
            start_stop = 0
        else:
            reset = 0
            phase = i % 500
            if phase == 0:
                reset = 1
                start_stop = 0
            elif phase == 1:
                reset = 0
                start_stop = 0
            elif phase < 60:
                reset = 0
                start_stop = 1
            elif phase < 70:
                reset = 0
                start_stop = 0
            elif phase < 130:
                reset = 0
                start_stop = 1
            elif phase < 140:
                reset = 0
                start_stop = 0
            elif phase < 200:
                reset = 0
                start_stop = 1
            elif phase < 210:
                reset = 0
                start_stop = 0
            elif phase < 270:
                reset = 0
                start_stop = 1
            elif phase < 280:
                reset = 0
                start_stop = 0
            elif phase < 340:
                reset = 0
                start_stop = 1
            elif phase < 350:
                reset = 0
                start_stop = 0
            elif phase < 410:
                reset = 0
                start_stop = 1
            elif phase < 420:
                reset = 0
                start_stop = 0
            elif phase < 480:
                reset = 0
                start_stop = 1
            else:
                reset = 0
                start_stop = 0
        row = {'reset': reset, 'start_stop': start_stop}
        if i > 10 and i % 17 == 0:
            row['mid'] = {'start_stop': rng.randint(0, 1)}
        rows.append(row)
    return rows
