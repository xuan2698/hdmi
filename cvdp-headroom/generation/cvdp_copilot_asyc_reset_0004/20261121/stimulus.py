def stimulus(rng, cycles):
    rows = []
    def row(r, mid=None):
        d = {'reset': r}
        if mid is not None:
            d['mid'] = mid
        rows.append(d)

    # Directed phase: reset asserted for several cycles
    for _ in range(4):
        row(1)
    # Full countdown from 31 to 0
    row(0)
    for _ in range(31):
        row(0)
    # Hold at zero a few cycles
    for _ in range(3):
        row(0)
    # Mid-count reset at cnt=15 (after 16 decrements from 31)
    row(1)
    row(0)
    for _ in range(16):
        row(0)
    row(1)  # reset at cnt=15
    row(0)
    # Reset at cnt=14 (gate boundary)
    for _ in range(17):
        row(0)
    row(1)
    row(0)
    # Reset at cnt=8 (release boundary)
    for _ in range(23):
        row(0)
    row(1)
    row(0)
    # Full countdown again
    for _ in range(32):
        row(0)
    # Reset during critical transition using mid
    row(0, {'reset': 1})
    row(0)
    row(1)
    row(0)
    # Mid-cycle reset pulses
    for _ in range(5):
        row(0, {'reset': 1})
        row(0)
    # Random exploration
    while len(rows) < cycles:
        r = 1 if rng.random() < 0.15 else 0
        if rng.random() < 0.2:
            row(r, {'reset': 1 if rng.random() < 0.5 else 0})
        else:
            row(r)
    return rows[:cycles]
