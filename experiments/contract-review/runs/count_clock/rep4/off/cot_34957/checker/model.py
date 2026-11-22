def reference(vectors):
    # State: hh, mm, ss as BCD ints; pm bit. Power-up unspecified -> start at 12:00 AM.
    hh, mm, ss, pm = 0x12, 0x00, 0x00, 0
    out = []
    for row in vectors:
        # Latch pre-edge inputs
        reset = row.get('reset', 0)
        ena = row.get('ena', 0)
        # Apply reset (highest priority) or enable
        if reset:
            hh, mm, ss, pm = 0x12, 0x00, 0x00, 0
        elif ena:
            # Increment seconds
            if ss == 0x59:
                ss = 0x00
                if mm == 0x59:
                    mm = 0x00
                    # Hour increment with 12-hour BCD rules
                    if hh == 0x12:
                        hh = 0x01
                        # pm holds on 12->1
                    elif hh == 0x11:
                        hh = 0x12
                        pm = 1 - pm  # toggle on 11->12
                    else:
                        # 01..09 -> next, 10 -> 11
                        hh = hh + 1
                else:
                    mm = mm + 1
            else:
                ss = ss + 1
        out.append({'pm': pm, 'hh': hh, 'mm': mm, 'ss': ss})
    return out
