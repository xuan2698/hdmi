def reference(vectors):
    # Contract implementation.
    # State: 4 BCD digits packed in q[15:0].
    # R1_reset: synchronous active-high reset -> q=0, ena=0 (same cycle visible).
    # R2_ones_count / R3_ones_wrap: ones digit counts 0..9 then wraps.
    # R4_tens_increment / R5_tens_wrap: tens increments when ones==9.
    # R6_hundreds_increment: hundreds increments when tens&ones==9.
    # R7_thousands_increment: thousands increments when hundreds&tens&ones==9.
    # R8_full_wrap: full 9999 -> 0000 wrap.
    # R9_ena_tens: ena[0] = (ones==9).
    # R10_ena_hundreds: ena[1] = (ones==9 and tens==9).
    # R11_ena_thousands: ena[2] = (ones==9 and tens==9 and hundreds==9).
    # Mid changes occur after sampling, carried to next row.

    q = 0  # internal state (16-bit BCD)
    out = []

    for row in vectors:
        reset = row.get("reset", 0)

        # Compute combinational outputs based on current state (before edge).
        # R9_ena_tens, R10_ena_hundreds, R11_ena_thousands
        d0 = q & 0xF
        d1 = (q >> 4) & 0xF
        d2 = (q >> 8) & 0xF
        d3 = (q >> 12) & 0xF

        ena_tens = 1 if d0 == 9 else 0
        ena_hundreds = 1 if (d0 == 9 and d1 == 9) else 0
        ena_thousands = 1 if (d0 == 9 and d1 == 9 and d2 == 9) else 0
        ena = (ena_thousands << 2) | (ena_hundreds << 1) | ena_tens

        # Sample outputs at posedge (current state visible this cycle).
        out.append({"q": q & 0xFFFF, "ena": ena & 0x7})

        # Update state at posedge.
        if reset:
            # R1_reset
            q = 0
        else:
            # R2_ones_count / R3_ones_wrap
            if d0 != 9:
                d0_new = d0 + 1
                d1_new, d2_new, d3_new = d1, d2, d3
            else:
                d0_new = 0
                # R4_tens_increment / R5_tens_wrap
                if d1 != 9:
                    d1_new = d1 + 1
                    d2_new, d3_new = d2, d3
                else:
                    d1_new = 0
                    # R6_hundreds_increment
                    if d2 != 9:
                        d2_new = d2 + 1
                        d3_new = d3
                    else:
                        d2_new = 0
                        # R7_thousands_increment / R8_full_wrap
                        if d3 != 9:
                            d3_new = d3 + 1
                        else:
                            d3_new = 0
            q = (d3_new << 12) | (d2_new << 8) | (d1_new << 4) | d0_new

    return out
