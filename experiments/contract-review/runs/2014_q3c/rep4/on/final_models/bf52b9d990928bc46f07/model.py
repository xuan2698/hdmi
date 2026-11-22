def reference(vectors):
    results = []
    for v in vectors:
        x = v['x']
        y = v['y']
        Y0 = 0
        z = 0
        if y == 0:
            if x == 0:
                # Y0_z_S0_x0
                Y0 = 0
                z = 0
            else:
                # Y0_z_S0_x1
                Y0 = 1
                z = 0
        elif y == 1:
            if x == 0:
                # Y0_z_S1_x0
                Y0 = 1
                z = 0
            else:
                # Y0_z_S1_x1
                Y0 = 0
                z = 0
        elif y == 2:
            if x == 0:
                # Y0_z_S2_x0
                Y0 = 0
                z = 0
            else:
                # Y0_z_S2_x1
                Y0 = 1
                z = 0
        elif y == 3:
            if x == 0:
                # Y0_z_S3_x0
                Y0 = 1
                z = 1
            else:
                # Y0_z_S3_x1
                Y0 = 0
                z = 1
        elif y == 4:
            if x == 0:
                # Y0_z_S4_x0
                Y0 = 1
                z = 1
            else:
                # Y0_z_S4_x1
                Y0 = 0
                z = 1
        else:
            # Y0_z_unused
            Y0 = 0
            z = 0
        results.append({'Y0': Y0, 'z': z})
    return results
