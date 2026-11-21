def stimulus(rng, cycles):
    rows = []
    # Phase plan: reset, directed token walk, data bursts, idle, random, reset injections
    for i in range(cycles):
        row = {}
        # Reset pattern: assert at start, occasionally mid-run, and near end
        if i == 0:
            rst = 1
        elif i < 4:
            rst = 0
        elif i % 97 == 0:
            rst = 1
        elif i % 97 == 1:
            rst = 0
        else:
            rst = 0

        # Directed data patterns
        phase = i % 64
        if phase < 8:
            # token walk with no data
            data_in = 0
            has = 0
        elif phase < 16:
            # data present every cycle
            data_in = (i * 3 + 1) & 0xF
            has = 1
        elif phase < 24:
            # alternating has_data
            data_in = (i * 5 + 2) & 0xF
            has = i & 1
        elif phase < 32:
            # walking data bits
            data_in = 1 << ((i // 2) % 4)
            has = 1
        elif phase < 40:
            # all ones / all zeros
            data_in = 0xF if (i & 2) else 0x0
            has = 1
        elif phase < 48:
            # idle
            data_in = 0
            has = 0
        elif phase < 56:
            # random-ish but seeded
            data_in = rng.randrange(16)
            has = rng.randrange(2)
        else:
            # burst then idle
            data_in = (i * 7) & 0xF
            has = 1 if (i % 4) < 2 else 0

        # Occasionally force random data regardless of phase
        if rng.random() < 0.15:
            data_in = rng.randrange(16)
        if rng.random() < 0.15:
            has = rng.randrange(2)

        row['rst'] = rst
        row['data_in'] = data_in & 0xF
        row['has_data_to_send'] = has & 1

        # Mid-cycle changes: toggle has_data or data_in sometimes
        if rng.random() < 0.25:
            mid = {}
            if rng.random() < 0.5:
                mid['has_data_to_send'] = rng.randrange(2)
            if rng.random() < 0.5:
                mid['data_in'] = rng.randrange(16)
            if mid:
                row['mid'] = mid

        rows.append(row)
    return rows
