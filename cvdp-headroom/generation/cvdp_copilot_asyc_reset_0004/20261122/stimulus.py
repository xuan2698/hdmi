def stimulus(rng, cycles):
    rows = []
    def row(r, mid=None):
        d = {'reset': r}
        if mid is not None:
            d['mid'] = mid
        rows.append(d)

    # Phase 1: reset asserted for several cycles
    for _ in range(4):
        row(1)

    # Phase 2: full countdown 31 -> 0 (32 cycles), then hold at 0
    row(0)
    for _ in range(31):
        row(0)
    for _ in range(4):
        row(0)

    # Phase 3: reset, then count to 0xF and reset mid-count
    row(1)
    row(0)
    for _ in range(16):  # 31 -> 15
        row(0)
    row(1)  # reset at cnt=0xF
    row(0)
    for _ in range(3):
        row(0)

    # Phase 4: reset, count through gate boundary 0xE->0xD
    row(1)
    row(0)
    for _ in range(17):  # 31 -> 14
        row(0)
    for _ in range(3):   # 14 -> 13 -> 12 -> 11
        row(0)

    # Phase 5: reset, count through release boundary 0x8->0x7
    row(1)
    row(0)
    for _ in range(23):  # 31 -> 8
        row(0)
    for _ in range(3):   # 8 -> 7 -> 6 -> 5
        row(0)

    # Phase 6: reset at cnt=0xE
    row(1)
    row(0)
    for _ in range(17):  # 31 -> 14
        row(0)
    row(1)  # reset at 0xE
    row(0)
    for _ in range(2):
        row(0)

    # Phase 7: reset at cnt=0x8
    row(1)
    row(0)
    for _ in range(23):  # 31 -> 8
        row(0)
    row(1)  # reset at 0x8
    row(0)
    for _ in range(2):
        row(0)

    # Phase 8: mid-cycle reset toggles (async behavior)
    row(1)
    row(0)
    for _ in range(5):
        row(0)
    row(0, {'reset': 1})  # assert reset mid-cycle
    row(0, {'reset': 0})  # deassert mid-cycle
    for _ in range(3):
        row(0)

    # Phase 9: random exploration
    while len(rows) < cycles:
        r = 1 if rng.random() < 0.15 else 0
        if rng.random() < 0.2:
            mr = 1 if rng.random() < 0.5 else 0
            row(r, {'reset': mr})
        else:
            row(r)

    return rows[:cycles]
