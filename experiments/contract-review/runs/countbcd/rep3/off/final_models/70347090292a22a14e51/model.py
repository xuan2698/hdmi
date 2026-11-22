def reference(vectors):
    # State: 4-digit BCD counter value (16 bits)
    # q[3:0]=ones, q[7:4]=tens, q[11:8]=hundreds, q[15:12]=thousands
    state = {"q": 0}
    out = []

    def digit(q, i):
        return (q >> (4 * i)) & 0xF

    def set_digit(q, i, v):
        return (q & ~(0xF << (4 * i))) | ((v & 0xF) << (4 * i))

    def compute_ena(q):
        # R2_ones_ena: ena[0] always 1 when reset==0
        ones = digit(q, 0)
        tens = digit(q, 1)
        hundreds = digit(q, 2)
        ena0 = 1
        # R3_tens_ena: ena[1] = 1 iff ones==9
        ena1 = 1 if ones == 9 else 0
        # R4_hundreds_ena: ena[2] = 1 iff ones==9 and tens==9
        ena2 = 1 if (ones == 9 and tens == 9) else 0
        return (ena2 << 2) | (ena1 << 1) | ena0

    for vec in vectors:
        reset = vec.get("reset", 0)

        # R1_reset: synchronous active-high reset -> outputs q=0, ena=0 same cycle
        if reset == 1:
            # R1_reset: visible same_cycle
            out.append({"q": 0, "ena": 0})
            # state update on posedge with reset: update_during_reset false -> q stays 0
            state["q"] = 0
            continue

        # reset == 0: combinational outputs based on current state
        q = state["q"]
        ena = compute_ena(q)  # R2_ones_ena, R3_tens_ena, R4_hundreds_ena
        out.append({"q": q, "ena": ena})

        # R5_count: posedge update
        ones = digit(q, 0)
        tens = digit(q, 1)
        hundreds = digit(q, 2)
        thousands = digit(q, 3)

        new_q = q
        # ones always increments
        new_ones = (ones + 1) % 10
        new_q = set_digit(new_q, 0, new_ones)
        if ones == 9:
            new_tens = (tens + 1) % 10
            new_q = set_digit(new_q, 1, new_tens)
            if tens == 9:
                new_hundreds = (hundreds + 1) % 10
                new_q = set_digit(new_q, 2, new_hundreds)
                if hundreds == 9:
                    new_thousands = (thousands + 1) % 10
                    new_q = set_digit(new_q, 3, new_thousands)
        state["q"] = new_q

    return out
