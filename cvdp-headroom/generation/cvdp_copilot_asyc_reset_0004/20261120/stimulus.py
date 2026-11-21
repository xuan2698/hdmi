def stimulus(rng, cycles):
    rows = []
    # Phase plan: list of (length, reset_value) segments
    # reset=1 holds counter at 31; reset=0 lets it count down.
    plan = []
    # 1. Initial reset for several cycles
    plan.append((8, 1))
    # 2. Full countdown from 31 to 0 (32 cycles) plus hold at 0
    plan.append((40, 0))
    # 3. Reset again, then countdown to mid-count (15) then reset
    plan.append((4, 1))
    plan.append((16, 0))   # 31 down to 16 (16 cycles) -> cnt=15
    plan.append((3, 1))    # reset at cnt=15
    plan.append((20, 0))   # countdown again
    # 4. Reset at cnt=14 (gate boundary) - count 17 cycles from 31 -> 14
    plan.append((3, 1))
    plan.append((17, 0))
    plan.append((2, 1))
    # 5. Reset at cnt=8 (release boundary) - count 23 cycles from 31 -> 8
    plan.append((3, 1))
    plan.append((23, 0))
    plan.append((2, 1))
    # 6. Full countdown to zero and hold
    plan.append((3, 1))
    plan.append((45, 0))
    # 7. Random exploration: random reset pulses and gaps
    # We'll fill remaining cycles with random reset toggling
    # First, compute how many cycles used so far
    used = sum(p[0] for p in plan)
    remaining = cycles - used
    # Build rows from plan
    for length, rv in plan:
        for _ in range(length):
            if len(rows) >= cycles:
                break
            rows.append({'reset': rv})
    # Random exploration for remaining cycles
    # Use a mix: random reset with bias toward 0 (counting) and occasional 1
    while len(rows) < cycles:
        # Occasionally do a burst of reset
        if rng.random() < 0.15:
            burst = rng.randint(1, 5)
            for _ in range(burst):
                if len(rows) >= cycles:
                    break
                rows.append({'reset': 1})
        else:
            # Random run of no-reset, length 1..40
            run = rng.randint(1, 40)
            for _ in range(run):
                if len(rows) >= cycles:
                    break
                rows.append({'reset': 0})
    # Trim or pad to exactly cycles
    rows = rows[:cycles]
    while len(rows) < cycles:
        rows.append({'reset': 0})
    return rows
