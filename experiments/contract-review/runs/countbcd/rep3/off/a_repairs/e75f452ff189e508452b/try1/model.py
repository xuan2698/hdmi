def reference(vectors):
    # State: 4-digit BCD counter value (16 bits)
    # q[3:0]=ones, q[7:4]=tens, q[11:8]=hundreds, q[15:12]=thousands
    state = {"q": 0}
    out = []

    def decode(q):
        ones = q & 0xF
        tens = (q >> 4) & 0xF
        hundreds = (q >> 8) & 0xF
        thousands = (q >> 12) & 0xF
        return ones, tens, hundreds, thousands

    def encode(ones, tens, hundreds, thousands):
        return (ones & 0xF) | ((tens & 0xF) << 4) | ((hundreds & 0xF) << 8) | ((thousands & 0xF) << 12)

    def compute_ena(q):
        # R2_ones_ena: ena[0] always 1 when not reset
        # R3_tens_ena: ena[1] = 1 iff ones == 9
        # R4_hundreds_ena: ena[2] = 1 iff ones==9 and tens==9
        ones, tens, hundreds, thousands = decode(q)
        ena0 = 1
        ena1 = 1 if ones == 9 else 0
        ena2 = 1 if (ones == 9 and tens == 9) else 0
        return (ena0) | (ena1 << 1) | (ena2 << 2)

    for vec in vectors:
        reset = vec.get("reset", 0)

        # R1_reset: synchronous active-high reset -> outputs q=0, ena=0
        if reset == 1:
            # R1_reset: reset visible same cycle
            out.append({"q": 0, "ena": 0})
            # state update on posedge: reset clears counter
            state["q"] = 0
            continue

        # Non-reset: compute combinational outputs from current state
        q = state["q"]
        ena = compute_ena(q)  # R2_ones_ena, R3_tens_ena, R4_hundreds_ena
        out.append({"q": q, "ena": ena})

        # R5_count: on posedge, increment BCD digits based on enables
        ones, tens, hundreds, thousands = decode(q)
        # ones always increments
        new_ones = (ones + 1) % 10
        # tens increments iff ones == 9
        if ones == 9:
            new_tens = (tens + 1) % 10
        else:
            new_tens = tens
        # hundreds increments iff ones==9 and tens==9
        if ones == 9 and tens == 9:
            new_hundreds = (hundreds + 1) % 10
        else:
            new_hundreds = hundreds
        # thousands increments iff ones==9, tens==9, hundreds==9
        if ones == 9 and tens == 9 and hundreds == 9:
            new_thousands = (thousands + 1) % 10
        else:
            new_thousands = thousands

        state["q"] = encode(new_ones, new_tens, new_hundreds, new_thousands)

    return out
