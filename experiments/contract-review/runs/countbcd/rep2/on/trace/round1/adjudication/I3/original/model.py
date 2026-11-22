def reference(vectors):
    # R_RESET: synchronous active-high reset forces q = 0x0000 at posedge.
    # R_COUNT_BCD: otherwise increment 4-digit BCD modulo 10000.
    # R_ENA_COMB: ena is combinational from current q (post-edge state).
    q = 0
    reset = 0
    outputs = []
    for row in vectors:
        # Drive inputs before the sampled posedge.
        try:
            reset = row['reset'] & 1
        except:
            try:
                reset = row[0] & 1
            except:
                pass

        # Sampled posedge.
        if reset:
            q = 0  # R_RESET
        else:
            # R_COUNT_BCD: increment packed BCD.
            ones = q & 0xF
            tens = (q >> 4) & 0xF
            hundreds = (q >> 8) & 0xF
            thousands = (q >> 12) & 0xF
            ones += 1
            if ones == 10:
                ones = 0
                tens += 1
                if tens == 10:
                    tens = 0
                    hundreds += 1
                    if hundreds == 10:
                        hundreds = 0
                        thousands += 1
                        if thousands == 10:
                            thousands = 0
            q = (thousands << 12) | (hundreds << 8) | (tens << 4) | ones

        # R_ENA_COMB: combinational enable from current q.
        ena = 0
        if (q & 0xF) == 9:
            ena += 1
        if (q & 0xFF) == 0x99:
            ena += 2
        if (q & 0xFFF) == 0x999:
            ena += 4

        outputs.append({'q': q, 'ena': ena})

        # Optional mid changes occur after sampling and carry to next row.
        try:
            mid = row['mid']
            try:
                reset = mid['reset'] & 1
            except:
                try:
                    reset = mid & 1
                except:
                    pass
        except:
            pass
        try:
            reset = row['reset_mid'] & 1
        except:
            pass
        try:
            reset = row['mid_reset'] & 1
        except:
            pass

    return outputs
