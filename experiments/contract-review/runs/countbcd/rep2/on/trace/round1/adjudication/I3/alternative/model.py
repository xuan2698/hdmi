def reference(vectors):
    # R_RESET and R_COUNT_BCD (with candidate decrement interpretation)
    count = 0
    reset_val = 0
    results = []
    for row in vectors:
        # Apply primary inputs before sampled posedge
        if 'reset' in row:
            reset_val = row['reset']
        # Sampled posedge
        if reset_val == 1:
            # R_RESET: synchronous active-high reset forces count to 0 (q=0x0000)
            count = 0
        else:
            # R_COUNT_BCD candidate interpretation: decrement by 1, wrap 0000 to 9999
            count = (count - 1) % 10000
        # Pack BCD into q
        ones = count % 10
        tens = (count // 10) % 10
        hundreds = (count // 100) % 10
        thousands = (count // 1000) % 10
        q = (thousands << 12) | (hundreds << 8) | (tens << 4) | ones
        # R_ENA_COMB: combinational enable from current q
        ena = 0
        if (q & 15) == 9:
            ena += 1
        if (q & 255) == 0x99:
            ena += 2
        if (q & 4095) == 0x999:
            ena += 4
        results.append({'q': q, 'ena': ena})
        # Process mid changes after sampling
        if 'mid' in row:
            mid = row['mid']
            for k in mid:
                if k == 'reset':
                    reset_val = mid[k]
        # Support direct *_mid keys
        for k in row:
            if k == 'reset_mid':
                reset_val = row[k]
    return results
