def stimulus(rng, cycles):
    rows = []
    reset = 1
    # Phase 1: hold reset for several cycles
    for _ in range(8):
        rows.append({'reset': 1})
    # Phase 2: full countdown from 31 to 0 (32 cycles)
    for _ in range(32):
        rows.append({'reset': 0})
    # Phase 3: hold at zero for a while
    for _ in range(6):
        rows.append({'reset': 0})
    # Phase 4: reset again, then countdown to mid-count reset at 15
    for _ in range(4):
        rows.append({'reset': 1})
    for _ in range(16):  # 31 down to 16
        rows.append({'reset': 0})
    # reset at cnt=15
    rows.append({'reset': 1})
    rows.append({'reset': 1})
    # countdown again, reset at cnt=14 (gate boundary)
    for _ in range(17):  # 31 down to 15
        rows.append({'reset': 0})
    rows.append({'reset': 1})
    # countdown, reset at cnt=8 (release boundary)
    for _ in range(23):  # 31 down to 9
        rows.append({'reset': 0})
    rows.append({'reset': 1})
    # full countdown with mid-cycle reset toggles
    for _ in range(32):
        rows.append({'reset': 0})
    # random exploration
    while len(rows) < cycles:
        r = rng.random()
        if r < 0.15:
            rows.append({'reset': 1})
        elif r < 0.25:
            # mid-cycle reset pulse
            rows.append({'reset': 0, 'mid': {'reset': 1}})
        elif r < 0.35:
            rows.append({'reset': 1, 'mid': {'reset': 0}})
        else:
            rows.append({'reset': 0})
    return rows[:cycles]
