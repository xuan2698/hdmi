def reference(vectors):
    # rule valid_y_0_to_4: Evaluate combinational logic for valid present states y=000..100.
    result = []
    for v in vectors:
        x = int(v.get('x', 0)) & 1
        y = int(v.get('y', 0)) & 7

        if y <= 4:
            y0 = (y >> 0) & 1
            y1 = (y >> 1) & 1
            y2 = (y >> 2) & 1

            Y0 = ((1 - x) & y0) | ((1 - x) & y2) | (x & (1 - y2) & (1 - y0))
            z = y2 | (y1 & y0)

            Y0 = 1 if Y0 else 0
            z = 1 if z else 0
        else:
            # global: treat unused present states as undefined; use concrete 0.
            Y0 = 0
            z = 0

        result.append({'Y0': Y0, 'z': z})

    return result
