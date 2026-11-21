def stimulus(rng, cycles):
    rows = []
    rst_n = 0
    start = 0
    enable = 0
    mode = 0
    clear = 0
    a = 0
    b = 0
    for i in range(cycles):
        # Reset phase
        if i < 4:
            rst_n = 0
            start = 0
            enable = 0
            mode = 0
            clear = 0
            a = 0
            b = 0
        else:
            rst_n = 1
            # Periodic clear pulses
            if i % 500 == 0:
                clear = 1
            else:
                clear = 0
            # Random control signals
            if rng.random() < 0.15:
                start = 1
            else:
                start = 0
            if rng.random() < 0.85:
                enable = 1
            else:
                enable = 0
            if rng.random() < 0.5:
                mode = 1
            else:
                mode = 0
            # Operand values
            a = rng.randrange(256)
            b = rng.randrange(256)
        row = {
            'i_rst_n': rst_n,
            'i_start': start,
            'i_enable': enable,
            'i_mode': mode,
            'i_clear': clear,
            'i_operand_a': a,
            'i_operand_b': b,
        }
        # Mid-cycle overrides
        mid = {}
        if i >= 4 and rng.random() < 0.2:
            mid['i_start'] = rng.randrange(2)
            mid['i_enable'] = rng.randrange(2)
            mid['i_mode'] = rng.randrange(2)
            mid['i_clear'] = rng.randrange(2)
            mid['i_operand_a'] = rng.randrange(256)
            mid['i_operand_b'] = rng.randrange(256)
        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows
