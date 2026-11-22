def reference(vectors):
    # State: 4 BCD digits, each 0..9. q packs digit3..digit0.
    # Contract rules implemented with comments.
    d0 = 0
    d1 = 0
    d2 = 0
    d3 = 0
    out = []
    for row in vectors:
        reset = row.get("reset", 0)
        # R1_reset: synchronous active-high reset -> q=0, ena=0 (same cycle visible)
        # global interpretation: ena asynchronously reset to 0 when reset=1
        if reset == 1:
            d0 = d1 = d2 = d3 = 0
            q = 0
            ena = 0
            out.append({"q": q, "ena": ena})
            continue
        # Compute current outputs (combinational ena based on current state)
        # R9_ena_tens: ena[0] = (d0 == 9)
        # R10_ena_hundreds: ena[1] = (d0 == 9 and d1 == 9)
        # R11_ena_thousands: ena[2] = (d0 == 9 and d1 == 9 and d2 == 9)
        e0 = 1 if d0 == 9 else 0
        e1 = 1 if (d0 == 9 and d1 == 9) else 0
        e2 = 1 if (d0 == 9 and d1 == 9 and d2 == 9) else 0
        ena = (e2 << 2) | (e1 << 1) | e0
        q = (d3 << 12) | (d2 << 8) | (d1 << 4) | d0
        out.append({"q": q, "ena": ena})
        # Next-state transitions at posedge (visible next cycle)
        # R2_ones_count / R3_ones_wrap: ones digit counts 0..9 then wraps
        if d0 != 9:
            d0 += 1  # R2_ones_count
        else:
            d0 = 0  # R3_ones_wrap
            # R4_tens_increment / R5_tens_wrap
            if d1 != 9:
                d1 += 1  # R4_tens_increment
            else:
                d1 = 0  # R5_tens_wrap
                # R6_hundreds_increment (and wrap)
                if d2 != 9:
                    d2 += 1  # R6_hundreds_increment
                else:
                    d2 = 0
                    # R7_thousands_increment / R8_full_wrap
                    if d3 != 9:
                        d3 += 1  # R7_thousands_increment
                    else:
                        d3 = 0  # R8_full_wrap
    return out
