def reference(vectors):
    # State: registered 16-bit BCD counter value
    q = 0
    out = []
    for row in vectors:
        # Read synchronous input value at the sampled posedge
        r = row["reset"] if "reset" in row else 0

        # rule reset: synchronous active-high reset has priority over increment
        if r == 1:
            q = 0
        else:
            # rule bcd_increment: BCD add 1 modulo 10000 with carry across nibbles
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

        # rule ena_combinational: reversed mapping
        # ena[2] = ones == 9
        # ena[1] = ones == 9 && tens == 9
        # ena[0] = ones == 9 && tens == 9 && hundreds == 9
        ones = q & 0xF
        tens = (q >> 4) & 0xF
        hundreds = (q >> 8) & 0xF

        ena = 0
        if ones == 9:
            ena = 4
            if tens == 9:
                ena = ena | 2
                if hundreds == 9:
                    ena = ena | 1

        out.append({"q": q, "ena": ena})

    return out
