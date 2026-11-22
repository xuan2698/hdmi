def reference(vectors):
    # rule reset: synchronous active-high reset; q and ena become 0
    # rule bcd_increment: BCD increment modulo 10000 with carry across nibbles
    # rule ena_combinational: ena bits derived combinationally from q after settle

    q = 0
    reset_in = 0
    out = []

    for row in vectors:
        # Each row's values are driven before the sampled posedge
        if "reset" in row:
            reset_in = row["reset"]

        # posedge clk: reset has priority over increment
        if reset_in == 1:
            q = 0
        else:
            # BCD increment
            ones = q & 0xF
            tens = (q >> 4) & 0xF
            hundreds = (q >> 8) & 0xF
            thousands = (q >> 12) & 0xF

            ones += 1
            carry = 0
            if ones == 10:
                ones = 0
                carry = 1

            tens += carry
            carry = 0
            if tens == 10:
                tens = 0
                carry = 1

            hundreds += carry
            carry = 0
            if hundreds == 10:
                hundreds = 0
                carry = 1

            thousands += carry
            if thousands == 10:
                thousands = 0

            q = (thousands << 12) | (hundreds << 8) | (tens << 4) | ones

        # combinational ena from q after settle
        ones = q & 0xF
        tens = (q >> 4) & 0xF
        hundreds = (q >> 8) & 0xF

        ena0 = 1 if ones == 9 else 0
        ena1 = 1 if (tens == 9 and ones == 9) else 0
        ena2 = 1 if (hundreds == 9 and tens == 9 and ones == 9) else 0
        ena = (ena2 << 2) | (ena1 << 1) | ena0

        out.append({"q": q, "ena": ena})

        # Optional mid input changes occur AFTER sampling, carried to next row
        if "mid" in row:
            mid = row["mid"]
            if "reset" in mid:
                reset_in = mid["reset"]

    return out
