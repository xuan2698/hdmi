def reference(vectors):
    # State: 4-digit BCD counter value (16 bits)
    # q[3:0]=ones, q[7:4]=tens, q[11:8]=hundreds, q[15:12]=thousands
    state = {"q": 0}

    def compute_ena(q):
        # R3_tens_ena: ena[0] = 1 iff ones digit == 9
        ones = q & 0xF
        tens = (q >> 4) & 0xF
        hundreds = (q >> 8) & 0xF
        ena0 = 1 if ones == 9 else 0
        # R4_hundreds_ena: ena[1] = 1 iff ones==9 and tens==9
        ena1 = 1 if (ones == 9 and tens == 9) else 0
        # ena[2] = 1 iff ones==9 and tens==9 and hundreds==9
        ena2 = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0
        return (ena2 << 2) | (ena1 << 1) | ena0

    def next_state(q):
        ones = q & 0xF
        tens = (q >> 4) & 0xF
        hundreds = (q >> 8) & 0xF
        thousands = (q >> 12) & 0xF
        # R5_count: increment each digit iff its enable is high
        if ones == 9:
            ones = 0
            if tens == 9:
                tens = 0
                if hundreds == 9:
                    hundreds = 0
                    if thousands == 9:
                        thousands = 0
                    else:
                        thousands += 1
                else:
                    hundreds += 1
            else:
                tens += 1
        else:
            ones += 1
        return (thousands << 12) | (hundreds << 8) | (tens << 4) | ones

    results = []
    for vec in vectors:
        reset = vec.get("reset", 0)
        # R1_reset: synchronous active-high reset; outputs visible same cycle
        # (reset affects state at posedge; outputs reflect current state)
        if reset == 1:
            # At posedge with reset, state becomes 0. Outputs visible same cycle.
            state["q"] = 0
            q_out = 0
            ena_out = 0
        else:
            # R3/R4: combinational ena based on current state
            q_out = state["q"]
            ena_out = compute_ena(q_out)
            # R5_count: posedge update (next_cycle visible)
            state["q"] = next_state(state["q"])
        results.append({"q": q_out & 0xFFFF, "ena": ena_out & 0x7})
    return results
