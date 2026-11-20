def stimulus(rng, cycles):
    rows = []

    def add(r, i):
        if len(rows) < cycles:
            rows.append({"reset": int(r), "in": int(i) & 0xFFFFFFFF})

    # Begin with synchronous active-high reset asserted to establish known state
    add(1, 0x00000000)
    add(1, 0xFFFFFFFF)

    # Release reset with all ones present
    add(0, 0xFFFFFFFF)

    # All bits experience 1 -> 0 (should capture every bit)
    add(0, 0x00000000)

    # Hold at zero (no new captures)
    add(0, 0x00000000)

    # Mid-stream reset clears captured bits
    add(1, 0xFFFFFFFF)
    add(1, 0x00000000)

    # Release reset again
    add(0, 0xFFFFFFFF)

    # Isolated single-bit 1 -> 0 transitions
    add(0, 0xFFFFFFFE)  # bit 0
    add(0, 0xFFFFFFFF)  # bit 0 goes 0 -> 1 (no capture)
    add(0, 0x7FFFFFFF)  # bit 31
    add(0, 0xFFFFFFFE)  # bit 0 again, bit 31 goes 0 -> 1

    # Alternating bit patterns to exercise many edges
    add(0, 0xAAAAAAAA)
    add(0, 0x55555555)  # odd bits 1 -> 0
    add(0, 0xAAAAAAAA)  # even bits 1 -> 0
    add(0, 0x00000000)
    add(0, 0xF0F0F0F0)
    add(0, 0x0F0F0F0F)
    add(0, 0x00000000)

    # Reset interaction near end of targeted sequence
    add(1, 0x00000000)
    add(0, 0xFFFFFFFF)

    # Pseudorandom inputs with occasional reset pulses
    while len(rows) < cycles:
        r = 1 if rng.random() < 0.08 else 0
        add(r, rng.getrandbits(32))

    return rows
