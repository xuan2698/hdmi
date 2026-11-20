def stimulus(rng, cycles):
    rows = []
    def add(r, i):
        rows.append({'reset': 1 if r else 0, 'in': int(i) & 0xFFFFFFFF})
    masks = [0x00000000, 0xFFFFFFFF, 0xAAAAAAAA, 0x55555555,
             0x80000000, 0x00000001, 0xFFFFFFFE, 0x7FFFFFFF,
             0xFFFFFFFD, 0xBFFFFFFF, 0x00000002, 0x40000000]
    # Reset to initialize known state
    add(1, 0)
    add(1, 0)
    # All 1s, hold, then fall to 0: capture all bits
    add(0, 0xFFFFFFFF)
    add(0, 0xFFFFFFFF)
    add(0, 0)
    add(0, 0)
    # Rise (no capture), fall alternating, rise, fall opposite
    add(0, 0xFFFFFFFF)
    add(0, 0xAAAAAAAA)
    add(0, 0)
    add(0, 0xFFFFFFFF)
    add(0, 0x55555555)
    add(0, 0)
    # Reset clears captures even though prev-in was all 1s
    add(1, 0xFFFFFFFF)
    add(0, 0)
    add(0, 0xFFFFFFFF)
    add(0, 0)
    # Single-bit falls
    add(0, 1); add(0, 0)
    add(0, 0x80000000); add(0, 0)
    add(0, 0x80000001); add(0, 0)
    # One-bit off from all 1s
    add(0, 0xFFFFFFFF); add(0, 0xFFFFFFFE)
    add(0, 0xFFFFFFFF); add(0, 0xFFFFFFFD)
    add(0, 0xFFFFFFFF); add(0, 0x7FFFFFFF)
    add(0, 0xFFFFFFFF); add(0, 0xBFFFFFFF)
    # Rapid toggling
    add(0, 0xFFFFFFFF); add(0, 0)
    add(0, 0xFFFFFFFF); add(0, 0)
    # Reset interaction with prev-in register
    add(1, 0x55555555)
    add(0, 0x55555555)
    add(0, 0)
    # Fill remaining cycles with pseudo-random stimulus
    while len(rows) < cycles:
        r = rng.random()
        if r < 0.1:
            add(1, rng.getrandbits(32))
        elif r < 0.5:
            add(0, rng.choice(masks))
        else:
            add(0, rng.getrandbits(32))
    return rows[:cycles]
