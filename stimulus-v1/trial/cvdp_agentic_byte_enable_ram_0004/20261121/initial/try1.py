def stimulus(rng, cycles):
    rows = []
    addr_a = 0
    addr_b = 0
    for i in range(cycles):
        # Reset-like initial phase: quiet first few cycles
        if i < 4:
            en_a = 0
            en_b = 0
            be_a = 0
            be_b = 0
            data_in_a = 0
            data_in_b = 0
            addr_a = 0
            addr_b = 0
        else:
            mode = rng.randrange(100)
            if mode < 30:
                # Idle
                en_a = 0
                en_b = 0
                be_a = 0
                be_b = 0
                data_in_a = 0
                data_in_b = 0
            elif mode < 55:
                # Port A write only
                en_a = 1
                en_b = 0
                be_a = rng.randrange(1, 16)
                be_b = 0
                addr_a = rng.randrange(8192)
                data_in_a = rng.randrange(1 << 32)
                data_in_b = 0
            elif mode < 75:
                # Port B write only
                en_a = 0
                en_b = 1
                be_a = 0
                be_b = rng.randrange(1, 16)
                addr_b = rng.randrange(8192)
                data_in_b = rng.randrange(1 << 32)
                data_in_a = 0
            elif mode < 90:
                # Both ports, different addresses
                en_a = 1
                en_b = 1
                be_a = rng.randrange(1, 16)
                be_b = rng.randrange(1, 16)
                addr_a = rng.randrange(8192)
                addr_b = rng.randrange(8192)
                if addr_a == addr_b:
                    addr_b = (addr_b + 1) % 8192
                data_in_a = rng.randrange(1 << 32)
                data_in_b = rng.randrange(1 << 32)
            else:
                # Collision: same address, both enabled
                en_a = 1
                en_b = 1
                be_a = rng.randrange(1, 16)
                be_b = rng.randrange(1, 16)
                addr_a = rng.randrange(8192)
                addr_b = addr_a
                data_in_a = rng.randrange(1 << 32)
                data_in_b = rng.randrange(1 << 32)

        row = {
            'addr_a': addr_a & 0x1FFF,
            'en_a': en_a & 1,
            'be_a': be_a & 0xF,
            'data_in_a': data_in_a & 0xFFFFFFFF,
            'addr_b': addr_b & 0x1FFF,
            'en_b': en_b & 1,
            'be_b': be_b & 0xF,
            'data_in_b': data_in_b & 0xFFFFFFFF,
        }
        rows.append(row)
    return rows
