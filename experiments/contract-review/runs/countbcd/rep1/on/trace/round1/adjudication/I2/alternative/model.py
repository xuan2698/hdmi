def reference(vectors):
    # Initial state: q and ena assumed 0 at power-up.
    q = 0
    ena = 0
    result = []

    for row in vectors:
        reset = row.get('reset', 0)

        if reset:
            # rule reset
            # Synchronous active-high reset: q becomes 0, ena becomes 0.
            q_next = 0
            ena_next = 0
        else:
            # rule ena_combinational (modified interpretation):
            # Register ena on posedge from current q (q before the edge).
            ones = q & 0xF
            tens = (q >> 4) & 0xF
            hundreds = (q >> 8) & 0xF
            e0 = 1 if ones == 9 else 0
            e1 = 1 if (tens == 9 and ones == 9) else 0
            e2 = 1 if (hundreds == 9 and tens == 9 and ones == 9) else 0
            ena_next = (e2 << 2) | (e1 << 1) | e0

            # rule bcd_increment
            # BCD add 1 modulo 10000 with carry across nibbles.
            d0 = q & 0xF
            d1 = (q >> 4) & 0xF
            d2 = (q >> 8) & 0xF
            d3 = (q >> 12) & 0xF

            carry = 1
            d0 += carry
            if d0 >= 10:
                d0 = 0
                carry = 1
            else:
                carry = 0

            if carry:
                d1 += 1
                if d1 >= 10:
                    d1 = 0
                    carry = 1
                else:
                    carry = 0

            if carry:
                d2 += 1
                if d2 >= 10:
                    d2 = 0
                    carry = 1
                else:
                    carry = 0

            if carry:
                d3 += 1
                if d3 >= 10:
                    d3 = 0
                    carry = 1
                else:
                    carry = 0

            # If carry remains after thousands, it wraps to 0000.
            q_next = (d3 << 12) | (d2 << 8) | (d1 << 4) | d0

        q = q_next
        ena = ena_next
        result.append({'q': q, 'ena': ena})

    return result
