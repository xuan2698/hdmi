def stimulus(rng, cycles):
    rows = []
    # Phase plan (in cycles): reset, run, pause, run, pause, reset, run
    # CLK_FREQ=200 -> 200 cycles per second. We use shorter runs to hit rollovers
    # via directed patterns plus random exploration.
    plan = []
    # initial reset
    plan.append(('reset', 3))
    # run long enough to cross second/minute boundaries (200 cycles/sec)
    plan.append(('run', 250))
    # pause
    plan.append(('pause', 20))
    # run to cross minute rollover (60 sec = 12000 cycles) - too long, so
    # instead use random exploration and shorter directed runs
    plan.append(('run', 400))
    # pause
    plan.append(('pause', 15))
    # reset during operation
    plan.append(('reset', 5))
    # run again
    plan.append(('run', 300))
    # random mixed phase
    plan.append(('random', 500))
    # final run
    plan.append(('run', 200))
    # fill remainder with random
    plan.append(('random', 10000))

    idx = 0
    for mode, count in plan:
        for _ in range(count):
            if idx >= cycles:
                break
            if mode == 'reset':
                reset = 1
                start_stop = rng.randint(0, 1)
            elif mode == 'run':
                reset = 0
                start_stop = 1
            elif mode == 'pause':
                reset = 0
                start_stop = 0
            else:  # random
                reset = 1 if rng.random() < 0.05 else 0
                start_stop = rng.randint(0, 1)
            row = {'reset': reset, 'start_stop': start_stop}
            # occasionally toggle start_stop mid-cycle
            if rng.random() < 0.1:
                row['mid'] = {'start_stop': rng.randint(0, 1)}
            rows.append(row)
            idx += 1
        if idx >= cycles:
            break

    # pad if needed
    while len(rows) < cycles:
        rows.append({'reset': 0, 'start_stop': rng.randint(0, 1)})

    return rows[:cycles]
