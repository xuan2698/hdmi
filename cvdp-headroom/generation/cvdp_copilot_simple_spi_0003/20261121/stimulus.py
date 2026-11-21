def stimulus(rng, cycles):
    rows = []
    # helper to build a row
    def row(rst=1, data=0, en=0, flt=0, clr=0, mid=None):
        d = {'i_rst_b': rst, 'i_data_in': data & 0xFFFF,
             'i_enable': en, 'i_fault': flt, 'i_clear': clr}
        if mid:
            d['mid'] = mid
        return d

    # Phase 1: reset and idle
    rows.append(row(rst=0, data=0, en=0, flt=0, clr=0))
    rows.append(row(rst=0, data=0xFFFF, en=1, flt=0, clr=0))
    rows.append(row(rst=1, data=0, en=0, flt=0, clr=0))
    rows.append(row(rst=1, data=0x1234, en=0, flt=0, clr=0))

    # Phase 2: normal transmissions with various data patterns
    patterns = [0x0000, 0xFFFF, 0x8000, 0x0001, 0xAAAA, 0x5555,
                0x1234, 0xDEAD, 0xBEEF, 0x00FF, 0xFF00, 0x000F]
    for p in patterns:
        # enable for a full transmission (~34 cycles: 16*2 + overhead)
        rows.append(row(rst=1, data=p, en=1, flt=0, clr=0))
        for _ in range(35):
            rows.append(row(rst=1, data=p, en=1, flt=0, clr=0))
        # brief disable
        rows.append(row(rst=1, data=p, en=0, flt=0, clr=0))
        rows.append(row(rst=1, data=p, en=0, flt=0, clr=0))

    # Phase 3: back-to-back transmissions without disabling
    for p in [0x1111, 0x2222, 0x4444, 0x8888]:
        rows.append(row(rst=1, data=p, en=1, flt=0, clr=0))
        for _ in range(34):
            rows.append(row(rst=1, data=p, en=1, flt=0, clr=0))

    # Phase 4: mid-cycle data changes during transmission
    rows.append(row(rst=1, data=0xABCD, en=1, flt=0, clr=0))
    for i in range(30):
        mid = {'i_data_in': (0xABCD ^ (i * 0x1111)) & 0xFFFF} if i % 3 == 0 else None
        rows.append(row(rst=1, data=0xABCD, en=1, flt=0, clr=0, mid=mid))

    # Phase 5: disable mid-transmission
    rows.append(row(rst=1, data=0xCAFE, en=1, flt=0, clr=0))
    for _ in range(8):
        rows.append(row(rst=1, data=0xCAFE, en=1, flt=0, clr=0))
    rows.append(row(rst=1, data=0xCAFE, en=0, flt=0, clr=0))
    rows.append(row(rst=1, data=0xCAFE, en=0, flt=0, clr=0))
    rows.append(row(rst=1, data=0xCAFE, en=1, flt=0, clr=0))
    for _ in range(35):
        rows.append(row(rst=1, data=0xCAFE, en=1, flt=0, clr=0))

    # Phase 6: clear mid-transmission
    rows.append(row(rst=1, data=0x9999, en=1, flt=0, clr=0))
    for _ in range(10):
        rows.append(row(rst=1, data=0x9999, en=1, flt=0, clr=0))
    rows.append(row(rst=1, data=0x9999, en=1, flt=0, clr=1))
    rows.append(row(rst=1, data=0x9999, en=1, flt=0, clr=0))
    rows.append(row(rst=1, data=0x9999, en=1, flt=0, clr=0))

    # Phase 7: fault injection and recovery
    rows.append(row(rst=1, data=0x7777, en=1, flt=0, clr=0))
    for _ in range(6):
        rows.append(row(rst=1, data=0x7777, en=1, flt=0, clr=0))
    rows.append(row(rst=1, data=0x7777, en=1, flt=1, clr=0))
    for _ in range(5):
        rows.append(row(rst=1, data=0x7777, en=1, flt=1, clr=0))
    # clear to exit error
    rows.append(row(rst=1, data=0x7777, en=1, flt=1, clr=1))
    rows.append(row(rst=1, data=0x7777, en=1, flt=0, clr=0))
    rows.append(row(rst=1, data=0x7777, en=1, flt=0, clr=0))
    # reset recovery
    rows.append(row(rst=0, data=0, en=0, flt=0, clr=0))
    rows.append(row(rst=1, data=0x7777, en=1, flt=0, clr=0))
    for _ in range(35):
        rows.append(row(rst=1, data=0x7777, en=1, flt=0, clr=0))

    # Phase 8: fault while idle
    rows.append(row(rst=1, data=0x0000, en=0, flt=1, clr=0))
    rows.append(row(rst=1, data=0x0000, en=0, flt=1, clr=0))
    rows.append(row(rst=1, data=0x0000, en=0, flt=1, clr=1))
    rows.append(row(rst=1, data=0x0000, en=0, flt=0, clr=0))

    # Phase 9: random exploration
    while len(rows) < cycles:
        rst = 1 if rng.random() > 0.02 else 0
        en = 1 if rng.random() > 0.25 else 0
        flt = 1 if rng.random() > 0.92 else 0
        clr = 1 if rng.random() > 0.93 else 0
        data = rng.getrandbits(16)
        mid = None
        if rng.random() > 0.85:
            mid = {'i_data_in': rng.getrandbits(16)}
        rows.append(row(rst=rst, data=data, en=en, flt=flt, clr=clr, mid=mid))

    return rows[:cycles]
