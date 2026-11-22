def reference(vectors):
    # Power-up is unspecified; use concrete zero state.
    count = 0
    q = 0
    ena = 0
    outputs = []

    for row in vectors:
        reset = int(row.get("reset", 0)) & 1

        # sync_active_high_reset: rising edge with reset=1 forces q=0 and ena=0.
        if reset:
            count = 0
            q = 0
            ena = 0
        else:
            # bcd_counter_increment: non-reset rising edge advances by one modulo 10000.
            count = (count + 1) % 10000
            ones = count % 10
            tens = (count // 10) % 10
            hundreds = (count // 100) % 10
            thousands = (count // 1000) % 10
            q = ones | (tens << 4) | (hundreds << 8) | (thousands << 12)

            # upper_digit_enables: combinational same-cycle enables based on current q.
            d0 = q & 0xF
            d1 = (q >> 4) & 0xF
            d2 = (q >> 8) & 0xF
            ena = 0
            if d0 == 9:
                ena |= 1
                if d1 == 9:
                    ena |= 2
                    if d2 == 9:
                        ena |= 4

        outputs.append({"q": q & 0xFFFF, "ena": ena & 0x7})

    return outputs
