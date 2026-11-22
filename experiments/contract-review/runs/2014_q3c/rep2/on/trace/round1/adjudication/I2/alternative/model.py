def reference(vectors):
    out = []
    for vec in vectors:
        x = int(vec.get('x', 0)) & 1
        y = int(vec.get('y', 0)) & 7
        if y <= 4:
            # valid_y_0_to_4
            y0_bit = y & 1
            y1_bit = (y >> 1) & 1
            y2_bit = (y >> 2) & 1
            if x == 0:
                Y0 = y0_bit | y2_bit
            else:
                Y0 = (1 - y2_bit) & (1 - y0_bit)
            z = y2_bit | (y1_bit & y0_bit)
        else:
            # unused_y_gt_4: treat unused present states as zero next-state bits with Y0=0 and z=0
            Y0 = 0
            z = 0
        out.append({'Y0': Y0 & 1, 'z': z & 1})
    return out
