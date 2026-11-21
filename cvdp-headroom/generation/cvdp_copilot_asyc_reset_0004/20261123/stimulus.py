def stimulus(rng, cycles):
    rows = []
    reset = 1
    # Phase 1: hold reset for several cycles
    for _ in range(6):
        rows.append({'reset': reset})
    reset = 0
    # Phase 2: full countdown from 31 to 0 (32 cycles), then hold at 0
    for _ in range(40):
        rows.append({'reset': reset})
    # Phase 3: mid-count reset at cnt=15 (after 16 decrements from 31)
    reset = 1
    rows.append({'reset': reset})
    reset = 0
    for _ in range(16):
        rows.append({'reset': reset})
    # assert reset when cnt should be 15
    reset = 1
    rows.append({'reset': reset})
    reset = 0
    # Phase 4: reset at cnt=14 (gate boundary) - 17 decrements from 31
    for _ in range(17):
        rows.append({'reset': reset})
    reset = 1
    rows.append({'reset': reset})
    reset = 0
    # Phase 5: reset at cnt=8 (release boundary) - 23 decrements from 31
    for _ in range(23):
        rows.append({'reset': reset})
    reset = 1
    rows.append({'reset': reset})
    reset = 0
    # Phase 6: full countdown again
    for _ in range(35):
        rows.append({'reset': reset})
    # Phase 7: random exploration
    while len(rows) < cycles:
        r = 1 if rng.random() < 0.15 else 0
        rows.append({'reset': r})
    return rows[:cycles]
