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
        # Reset phase: hold reset low for first 4 cycles
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
            # Enable mostly high, occasional low runs
            if (i % 200) < 10:
                enable = 0
            else:
                enable = 1
            # Start pulses to kick off transactions
            if (i % 37) == 0:
                start = 1
            else:
                start = 0
            # Mode toggling
            mode = (i // 23) & 1
            # Operand generation with varied patterns
            a = (i * 37 + 11) & 0xFF
            b = (i * 53 + 7) & 0xFF
            # Occasionally use extreme values
            if i % 97 == 0:
                a = 0x80
                b = 0x80
            elif i % 89 == 0:
                a = 0x7F
                b = 0x7F
            elif i % 83 == 0:
                a = 0xFF
                b = 0x01
        row = {
            'i_rst_n': rst_n,
            'i_start': start,
            'i_enable': enable,
            'i_mode': mode,
            'i_clear': clear,
            'i_operand_a': a,
            'i_operand_b': b,
        }
        # Mid-cycle overrides: sometimes change operands after rising edge
        if i >= 4 and (i % 41) == 0:
            row['mid'] = {
                'i_operand_a': (a + 1) & 0xFF,
                'i_operand_b': (b + 2) & 0xFF,
            }
        rows.append(row)
    return rows
