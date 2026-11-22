def reference(vectors):
    q = 0
    current_inputs = {"reset": 0}
    outputs = []
    for row in vectors:
        inputs = {"reset": current_inputs.get("reset", 0)}
        if "reset" in row:
            inputs["reset"] = row["reset"]

        # q_sync_reset: synchronous active-high reset
        if inputs["reset"] == 1:
            q = 0
        else:
            # q_bcd_count: 4-digit BCD increment
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

        # ena_upper_digit_increment: combinational from settled q
        ones = q & 0xF
        tens = (q >> 4) & 0xF
        hundreds = (q >> 8) & 0xF
        ena0 = 1 if ones == 9 else 0
        ena1 = 1 if (ones == 9 and tens == 9) else 0
        ena2 = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0
        ena = ena0 | (ena1 << 1) | (ena2 << 2)

        outputs.append({"ena": ena, "q": q})

        # carry inputs and apply optional mid changes after sampling
        current_inputs = {"reset": inputs["reset"]}
        if "mid" in row:
            mid = row["mid"]
            if "reset" in mid:
                current_inputs["reset"] = mid["reset"]

    return outputs
