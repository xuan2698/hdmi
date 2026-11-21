def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i == 2:
            reset = 0
        if i == 4:
            start_stop = 1
        if i == 40:
            start_stop = 0
        if i == 45:
            start_stop = 1
        if i == 120:
            reset = 1
        if i == 123:
            reset = 0
        if i == 125:
            start_stop = 1
        if i == 200:
            start_stop = 0
        if i == 210:
            start_stop = 1
        if i == 300:
            reset = 1
        if i == 303:
            reset = 0
        if i == 305:
            start_stop = 1
        if i == 400:
            start_stop = 0
        if i == 420:
            start_stop = 1
        if i == 500:
            reset = 1
        if i == 503:
            reset = 0
        if i == 505:
            start_stop = 1
        if i == 600:
            start_stop = 0
        if i == 630:
            start_stop = 1
        if i == 700:
            reset = 1
        if i == 703:
            reset = 0
        if i == 705:
            start_stop = 1
        if i == 800:
            start_stop = 0
        if i == 840:
            start_stop = 1
        if i == 900:
            reset = 1
        if i == 903:
            reset = 0
        if i == 905:
            start_stop = 1
        if i == 1000:
            start_stop = 0
        if i == 1050:
            start_stop = 1
        if i == 1100:
            reset = 1
        if i == 1103:
            reset = 0
        if i == 1105:
            start_stop = 1
        if i == 1200:
            start_stop = 0
        if i == 1260:
            start_stop = 1
        if i == 1300:
            reset = 1
        if i == 1303:
            reset = 0
        if i == 1305:
            start_stop = 1
        if i == 1400:
            start_stop = 0
        if i == 1470:
            start_stop = 1
        if i == 1500:
            reset = 1
        if i == 1503:
            reset = 0
        if i == 1505:
            start_stop = 1
        if i == 1600:
            start_stop = 0
        if i == 1680:
            start_stop = 1
        if i == 1700:
            reset = 1
        if i == 1703:
            reset = 0
        if i == 1705:
            start_stop = 1
        if i == 1800:
            start_stop = 0
        if i == 1890:
            start_stop = 1
        if i == 1900:
            reset = 1
        if i == 1903:
            reset = 0
        if i == 1905:
            start_stop = 1
        if i == 2000:
            start_stop = 0
        if i == 2100:
            start_stop = 1
        if i == 2100:
            reset = 1
        if i == 2103:
            reset = 0
        if i == 2105:
            start_stop = 1
        if i == 2200:
            start_stop = 0
        if i == 2310:
            start_stop = 1
        if i == 2300:
            reset = 1
        if i == 2303:
            reset = 0
        if i == 2305:
            start_stop = 1
        if i == 2400:
            start_stop = 0
        if i == 2520:
            start_stop = 1
        if i == 2500:
            reset = 1
        if i == 2503:
            reset = 0
        if i == 2505:
            start_stop = 1
        if i == 2600:
            start_stop = 0
        if i == 2730:
            start_stop = 1
        if i == 2700:
            reset = 1
        if i == 2703:
            reset = 0
        if i == 2705:
            start_stop = 1
        if i == 2800:
            start_stop = 0
        if i == 2940:
            start_stop = 1
        if i == 2900:
            reset = 1
        if i == 2903:
            reset = 0
        if i == 2905:
            start_stop = 1
        if i == 3000:
            start_stop = 0
        if i == 3150:
            start_stop = 1
        if i == 3100:
            reset = 1
        if i == 3103:
            reset = 0
        if i == 3105:
            start_stop = 1
        if i == 3200:
            start_stop = 0
        if i == 3360:
            start_stop = 1
        if i == 3300:
            reset = 1
        if i == 3303:
            reset = 0
        if i == 3305:
            start_stop = 1
        if i == 3400:
            start_stop = 0
        if i == 3570:
            start_stop = 1
        if i == 3500:
            reset = 1
        if i == 3503:
            reset = 0
        if i == 3505:
            start_stop = 1
        if i == 3600:
            start_stop = 0
        if i == 3780:
            start_stop = 1
        if i == 3700:
            reset = 1
        if i == 3703:
            reset = 0
        if i == 3705:
            start_stop = 1
        if i == 3800:
            start_stop = 0
        if i == 3990:
            start_stop = 1
        if i == 3900:
            reset = 1
        if i == 3903:
            reset = 0
        if i == 3905:
            start_stop = 1
        row = {'reset': reset, 'start_stop': start_stop}
        rows.append(row)
    return rows
