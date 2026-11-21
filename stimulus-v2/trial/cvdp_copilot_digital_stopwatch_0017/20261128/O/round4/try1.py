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
            reset = 0
            if i < 10:
                start_stop = 1
            elif i < 15:
                start_stop = 0
            elif i < 60:
                start_stop = 1
            elif i < 65:
                start_stop = 0
            elif i < 120:
                start_stop = 1
            elif i < 125:
                start_stop = 0
            elif i < 200:
                start_stop = 1
            elif i < 205:
                start_stop = 0
            elif i < 300:
                start_stop = 1
            elif i < 305:
                start_stop = 0
            elif i < 400:
                start_stop = 1
            elif i < 405:
                start_stop = 0
            elif i < 500:
                start_stop = 1
            elif i < 505:
                start_stop = 0
            elif i < 600:
                start_stop = 1
            elif i < 605:
                start_stop = 0
            elif i < 700:
                start_stop = 1
            elif i < 705:
                start_stop = 0
            elif i < 800:
                start_stop = 1
            elif i < 805:
                start_stop = 0
            elif i < 900:
                start_stop = 1
            elif i < 905:
                start_stop = 0
            elif i < 1000:
                start_stop = 1
            elif i < 1005:
                start_stop = 0
            elif i < 1100:
                start_stop = 1
            elif i < 1105:
                start_stop = 0
            elif i < 1200:
                start_stop = 1
            elif i < 1205:
                start_stop = 0
            elif i < 1300:
                start_stop = 1
            elif i < 1305:
                start_stop = 0
            elif i < 1400:
                start_stop = 1
            elif i < 1405:
                start_stop = 0
            elif i < 1500:
                start_stop = 1
            elif i < 1505:
                start_stop = 0
            elif i < 1600:
                start_stop = 1
            elif i < 1605:
                start_stop = 0
            elif i < 1700:
                start_stop = 1
            elif i < 1705:
                start_stop = 0
            elif i < 1800:
                start_stop = 1
            elif i < 1805:
                start_stop = 0
            elif i < 1900:
                start_stop = 1
            elif i < 1905:
                start_stop = 0
            elif i < 2000:
                start_stop = 1
            elif i < 2005:
                start_stop = 0
            elif i < 2100:
                start_stop = 1
            elif i < 2105:
                start_stop = 0
            elif i < 2200:
                start_stop = 1
            elif i < 2205:
                start_stop = 0
            elif i < 2300:
                start_stop = 1
            elif i < 2305:
                start_stop = 0
            elif i < 2400:
                start_stop = 1
            elif i < 2405:
                start_stop = 0
            elif i < 2500:
                start_stop = 1
            elif i < 2505:
                start_stop = 0
            elif i < 2600:
                start_stop = 1
            elif i < 2605:
                start_stop = 0
            elif i < 2700:
                start_stop = 1
            elif i < 2705:
                start_stop = 0
            elif i < 2800:
                start_stop = 1
            elif i < 2805:
                start_stop = 0
            elif i < 2900:
                start_stop = 1
            elif i < 2905:
                start_stop = 0
            elif i < 3000:
                start_stop = 1
            elif i < 3005:
                start_stop = 0
            elif i < 3100:
                start_stop = 1
            elif i < 3105:
                start_stop = 0
            elif i < 3200:
                start_stop = 1
            elif i < 3205:
                start_stop = 0
            elif i < 3300:
                start_stop = 1
            elif i < 3305:
                start_stop = 0
            elif i < 3400:
                start_stop = 1
            elif i < 3405:
                start_stop = 0
            elif i < 3500:
                start_stop = 1
            elif i < 3505:
                start_stop = 0
            elif i < 3600:
                start_stop = 1
            elif i < 3605:
                start_stop = 0
            elif i < 3700:
                start_stop = 1
            elif i < 3705:
                start_stop = 0
            elif i < 3800:
                start_stop = 1
            elif i < 3805:
                start_stop = 0
            elif i < 3900:
                start_stop = 1
            elif i < 3905:
                start_stop = 0
            elif i < 3990:
                start_stop = 1
            else:
                start_stop = 0
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows
