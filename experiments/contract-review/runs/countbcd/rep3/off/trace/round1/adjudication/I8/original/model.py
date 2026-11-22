def reference(vectors):
    # State: 4-digit BCD counter value (16 bits)
    # q[3:0]=ones, q[7:4]=tens, q[11:8]=hundreds, q[15:12]=thousands
    state = {"q": 0}

    def decode(q):
        ones = q & 0xF
        tens = (q >> 4) & 0xF
        hundreds = (q >> 8) & 0xF
        thousands = (q >> 12) & 0xF
        return ones, tens, hundreds, thousands

    def encode(ones, tens, hundreds, thousands):
        return (ones & 0xF) | ((tens & 0xF) << 4) | ((hundreds & 0xF) << 8) | ((thousands & 0xF) << 12)

    def compute_ena(q):
        # R2_ones_ena: ena[0] always 1 when reset==0
        # R3_tens_ena: ena[1] iff ones==9
        # R4_hundreds_ena: ena[2] iff ones==9 and tens==9
        ones, tens, hundreds, thousands = decode(q)
        ena0 = 1
        ena1 = 1 if ones == 9 else 0
        ena2 = 1 if (ones == 9 and tens == 9) else 0
        ena = ena0 | (ena1 << 1) | (ena2 << 2)
        return ena

    results = []
    for vec in vectors:
        reset = vec.get("reset", 0)

        # Compute outputs visible same cycle (combinational / registered current state)
        if reset == 1:
            # R1_reset: synchronous active-high reset -> outputs q=0, ena=0
            out_q = 0
            out_ena = 0
        else:
            out_q = state["q"]
            out_ena = compute_ena(state["q"])

        results.append({"q": out_q & 0xFFFF, "ena": out_ena & 0x7})

        # R5_count: posedge update
        if reset == 1:
            # R1_reset: reset during posedge -> q becomes 0
            state["q"] = 0
        else:
            ones, tens, hundreds, thousands = decode(state["q"])
            # ones always increments
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
            state["q"] = encode(ones, tens, hundreds, thousands)

    return results
