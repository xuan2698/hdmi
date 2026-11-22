def reference(vectors):
    # rule reset: synchronous active-high reset, priority over increment
    # rule bcd_increment: BCD add modulo 10000
    # rule ena_combinational: candidate interpretation applied, registered on posedge clk, one cycle delayed from q-based conditions
    q = 0
    ena = 0
    out = []
    for row in vectors:
        reset = row.get('reset', 0)
        if reset:
            # rule reset
            q_next = 0
            ena_next = 0
        else:
            # rule bcd_increment
            o0 = q & 0xF
            o1 = (q >> 4) & 0xF
            o2 = (q >> 8) & 0xF
            o3 = (q >> 12) & 0xF

            # rule ena_combinational (registered interpretation)
            ena_next = 0
            if o0 == 9:
                ena_next |= 1
            if o1 == 9 and o0 == 9:
                ena_next |= 2
            if o2 == 9 and o1 == 9 and o0 == 9:
                ena_next |= 4

            d0 = o0 + 1
            c0 = 0
            if d0 == 10:
                d0 = 0
                c0 = 1

            d1 = o1 + c0
            c1 = 0
            if d1 == 10:
                d1 = 0
                c1 = 1

            d2 = o2 + c1
            c2 = 0
            if d2 == 10:
                d2 = 0
                c2 = 1

            d3 = o3 + c2
            if d3 == 10:
                d3 = 0

            q_next = d0 | (d1 << 4) | (d2 << 8) | (d3 << 12)

        q = q_next & 0xFFFF
        ena = ena_next & 0x7
        out.append({'q': q, 'ena': ena})
    return out
