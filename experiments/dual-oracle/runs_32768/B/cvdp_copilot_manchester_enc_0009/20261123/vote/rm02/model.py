def reference(vectors):
    N = 8
    e_d = 0
    e_v = 0
    d_d = 0
    d_v = 0
    outs = []

    for i, row in enumerate(vectors):
        rst = int(row.get('rst_in', 0))

        if rst:
            e_d = e_v = d_d = d_v = 0

        outs.append({
            'enc_valid_out': e_v & 1,
            'enc_data_out': e_d & 0xFFFF,
            'dec_valid_out': d_v & 1,
            'dec_data_out': d_d & 0xFF
        })

        if i % 2 == 0:  # posedge
            if rst:
                e_d = e_v = d_d = d_v = 0
            else:
                ed_in = int(row.get('enc_data_in', 0))
                ev_in = int(row.get('enc_valid_in', 0))
                dd_in = int(row.get('dec_data_in', 0))
                dv_in = int(row.get('dec_valid_in', 0))

                e_next = 0
                for b in range(N):
                    bit = (ed_in >> b) & 1
                    pair = 1 if bit else 2  # 1 -> 01, 0 -> 10
                    e_next |= pair << (2 * b)

                d_next = 0
                for b in range(N):
                    pair = (dd_in >> (2 * b)) & 3
                    if pair == 1:  # 01 -> 1, everything else -> 0
                        d_next |= (1 << b)

                e_d = e_next & 0xFFFF
                e_v = ev_in & 1
                d_d = d_next & 0xFF
                d_v = dv_in & 1

    return outs
