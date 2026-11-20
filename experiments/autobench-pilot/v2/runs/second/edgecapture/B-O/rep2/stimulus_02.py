def stimulus(rng, cycles):
    out = []
    prev = 0
    for i in range(cycles):
        r = 0
        if i == 0:
            r = 1
        elif i == 1:
            r = 0
        elif i % 7 == 0:
            r = 1 if rng.random() < 0.3 else 0
        if r:
            val = 0
            if rng.random() < 0.5:
                val = rng.getrandbits(32)
            else:
                val = 0xFFFFFFFF
        else:
            if i < 4:
                val = 0xFFFFFFFF if i % 2 == 0 else 0
            else:
                mode = rng.randrange(4)
                if mode == 0:
                    val = rng.getrandbits(32)
                elif mode == 1:
                    val = prev ^ (1 << rng.randrange(32))
                elif mode == 2:
                    val = (prev << 1) & 0xFFFFFFFF
                else:
                    val = rng.choice([0, 0xFFFFFFFF, 0xAAAAAAAA, 0x55555555])
        out.append({'reset': r, 'in': val & 0xFFFFFFFF})
        prev = val & 0xFFFFFFFF
    return out
