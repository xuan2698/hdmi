def stimulus(rng, cycles):
    rows = []
    # Phase plan (in cycles). CLK_FREQ=200 -> 200 cycles per second.
    # We'll drive reset/start_stop to exercise: reset, run, pause, resume,
    # reset-during-run, run again, and random exploration.
    plan = []
    # initial reset asserted
    plan.append(('reset', 5))
    # run for ~1000 cycles (5 seconds)
    plan.append(('run', 1000))
    # pause 200 cycles
    plan.append(('pause', 200))
    # run 3000 cycles (15 seconds)
    plan.append(('run', 3000))
    # pause 500 cycles
    plan.append(('pause', 500))
    # reset during operation 5 cycles
    plan.append(('reset', 5))
    # run 100 cycles
    plan.append(('run', 100))
    # random exploration for the rest
    plan.append(('random', None))

    state = 'reset'
    remaining = 0
    idx = 0
    for i in range(cycles):
        if remaining == 0:
            if idx < len(plan):
                state, dur = plan[idx]
                idx += 1
                if dur is None:
                    remaining = cycles - i
                else:
                    remaining = dur
            else:
                state = 'random'
                remaining = cycles - i
        remaining -= 1

        if state == 'reset':
            reset = 1
            start_stop = 0
        elif state == 'run':
            reset = 0
            start_stop = 1
        elif state == 'pause':
            reset = 0
            start_stop = 0
        else:
            # random exploration: bias toward running, occasional resets
            r = rng.random()
            if r < 0.05:
                reset = 1
                start_stop = 0
            elif r < 0.15:
                reset = 0
                start_stop = 0
            else:
                reset = 0
                start_stop = 1

        row = {'reset': reset, 'start_stop': start_stop}
        # occasional mid-cycle toggles to stress async reset / control
        if rng.random() < 0.02:
            mid = {}
            if rng.random() < 0.5:
                mid['reset'] = 1 - reset
            if rng.random() < 0.5:
                mid['start_stop'] = 1 - start_stop
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows
