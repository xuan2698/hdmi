def reference(vectors):
    # State: 16-bit BCD counter value
    # q[3:0]=ones, q[7:4]=tens, q[11:8]=hundreds, q[15:12]=thousands
    state = {"q": 0}
    outputs = []

    for vec in vectors:
        reset = vec.get("reset", 0)

        # Compute outputs visible at this posedge (based on current state and reset)
        # R1_reset: synchronous active-high reset -> q=0, ena=0
        if reset == 1:
            q_out = 0
            ena_out = 0
        else:
            q_out = state["q"]
            ones = q_out & 0xF
            tens = (q_out >> 4) & 0xF
            hundreds = (q_out >> 8) & 0xF
            # R3_ena_tens: ena[0] when ones==9
            # R4_ena_hundreds: ena[1] when ones==9 and tens==9
            # R5_ena_thousands: ena[2] when ones==9 and tens==9 and hundreds==9
            e0 = 1 if ones == 9 else 0
            e1 = 1 if (ones == 9 and tens == 9) else 0
            e2 = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0
            ena_out = (e2 << 2) | (e1 << 1) | e0

        outputs.append({"q": q_out & 0xFFFF, "ena": ena_out & 0x7})

        # Update state at posedge
        if reset == 1:
            # R1_reset: update_during_reset false -> state stays 0
            state["q"] = 0
        else:
            # R2_ones_increment: ones increments every cycle including 9->0 wrap
            # R6_bcd_rollover: BCD rollover
            ones = state["q"] & 0xF
            tens = (state["q"] >> 4) & 0xF
            hundreds = (state["q"] >> 8) & 0xF
            thousands = (state["q"] >> 12) & 0xF

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

            state["q"] = (thousands << 12) | (hundreds << 8) | (tens << 4) | ones

    return outputs
