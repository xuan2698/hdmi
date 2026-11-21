def stimulus(rng, cycles):
    rows = []
    # Phase plan (in cycles):
    # 0-4: reset asserted
    # 5-9: idle (start_stop=0)
    # 10-19: start running
    # 20-24: stop
    # 25-34: run again
    # 35-39: reset pulse
    # 40-49: run
    # 50-54: stop
    # 55-64: run
    # 65-69: reset
    # 70-79: run
    # 80-84: stop
    # 85-94: run
    # 95-99: reset
    # 100+: random exploration with occasional directed bursts
    for i in range(cycles):
        if i < 5:
            reset = 1
            start_stop = 0
        elif i < 10:
            reset = 0
            start_stop = 0
        elif i < 20:
            reset = 0
            start_stop = 1
        elif i < 25:
            reset = 0
            start_stop = 0
        elif i < 35:
            reset = 0
            start_stop = 1
        elif i < 40:
            reset = 1
            start_stop = 0
        elif i < 50:
            reset = 0
            start_stop = 1
        elif i < 55:
            reset = 0
            start_stop = 0
        elif i < 65:
            reset = 0
            start_stop = 1
        elif i < 70:
            reset = 1
            start_stop = 0
        elif i < 80:
            reset = 0
            start_stop = 1
        elif i < 85:
            reset = 0
            start_stop = 0
        elif i < 95:
            reset = 0
            start_stop = 1
        elif i < 100:
            reset = 1
            start_stop = 0
        else:
            # Random exploration with weighted patterns
            r = rng.random()
            if r < 0.05:
                reset = 1
                start_stop = rng.randint(0, 1)
            elif r < 0.15:
                reset = 0
                start_stop = 0
            elif r < 0.25:
                reset = 0
                start_stop = 1
            else:
                # Long runs with occasional toggles
                reset = 0
                start_stop = 1 if (i // 7) % 2 == 0 else 0
        row = {'reset': reset, 'start_stop': start_stop}
        # Occasionally inject mid-cycle changes for temporal variety
        if i >= 100 and rng.random() < 0.1:
            mid = {}
            if rng.random() < 0.5:
                mid['start_stop'] = 1 - start_stop
            if rng.random() < 0.2:
                mid['reset'] = 1
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows
