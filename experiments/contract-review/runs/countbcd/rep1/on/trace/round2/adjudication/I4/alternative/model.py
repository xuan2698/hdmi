def reference(vectors):
    # rule reset, rule bcd_increment, rule ena_combinational
    # State: registered BCD counter value and carried input value.
    # Power-up unspecified, choose deterministic initial values.
    q = 0
    carried_reset = 0
    outputs = []

    def extract_pre_mid(v):
        # Try sequence form: [pre, mid]
        try:
            pre = v[0]
        except:
            pre = None
        if pre is not None:
            try:
                mid = v[1]
            except:
                mid = pre
            return pre, mid
        # Try dict form: {'pre': pre, 'mid': mid}
        try:
            pre = v['pre']
        except:
            pre = None
        if pre is not None:
            try:
                mid = v['mid']
            except:
                mid = pre
            return pre, mid
        # Constant value for the whole cycle
        return v, v

    for row in vectors:
        # Determine reset value before the sampled posedge.
        if 'reset' in row:
            pre_reset, mid_reset_value = extract_pre_mid(row['reset'])
        else:
            pre_reset = carried_reset
            mid_reset_value = carried_reset

        # Apply any explicit mid change that occurs after sampling.
        mid_reset = mid_reset_value
        if 'mid' in row:
            try:
                if 'reset' in row['mid']:
                    mid_reset = row['mid']['reset']
            except:
                pass
        if 'reset_mid' in row:
            mid_reset = row['reset_mid']

        # rule reset: synchronous active-high reset has priority over increment.
        # rule bcd_increment: BCD add 1 modulo 10000 when reset low.
        if pre_reset:
            q = 0
        else:
            ones = q & 0xF
            tens = (q >> 4) & 0xF
            hundreds = (q >> 8) & 0xF
            thousands = (q >> 12) & 0xF

            ones = ones + 1
            if ones == 10:
                ones = 0
                tens = tens + 1
                if tens == 10:
                    tens = 0
                    hundreds = hundreds + 1
                    if hundreds == 10:
                        hundreds = 0
                        thousands = thousands + 1
                        if thousands == 10:
                            thousands = 0
            q = ones | (tens << 4) | (hundreds << 8) | (thousands << 12)

        # rule ena_combinational: combinational from q after the edge,
        # with reversed ena bit mapping as specified.
        ones = q & 0xF
        tens = (q >> 4) & 0xF
        hundreds = (q >> 8) & 0xF

        ena = 0
        if ones == 9:
            ena = ena | 4       # ena[2]
        if tens == 9 and ones == 9:
            ena = ena | 2       # ena[1]
        if hundreds == 9 and tens == 9 and ones == 9:
            ena = ena | 1       # ena[0]

        outputs.append({'q': q, 'ena': ena})

        # Mid changes are applied after sampling and carried to next row.
        carried_reset = mid_reset

    return outputs
