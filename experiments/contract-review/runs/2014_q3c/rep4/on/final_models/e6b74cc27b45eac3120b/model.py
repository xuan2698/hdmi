def reference(vectors):
    results = []
    for v in vectors:
        x = v["x"]
        y = v["y"]
        if y == 0:
            # Y0_z_S0_x0, Y0_z_S0_x1: y=0 -> Y0=x, z=0
            Y0 = x
            z = 0
        elif y == 1:
            # Y0_z_S1_x0, Y0_z_S1_x1: y=1 -> Y0=~x, z=0
            Y0 = 1 - x
            z = 0
        elif y == 2:
            # Y0_z_S2_x0, Y0_z_S2_x1: y=2 -> Y0=x, z=0
            Y0 = x
            z = 0
        elif y == 3:
            # Y0_z_S3_x0, Y0_z_S3_x1: y=3 -> Y0=~x, z=1
            Y0 = 1 - x
            z = 1
        elif y == 4:
            # Y0_z_S4_x0, Y0_z_S4_x1: y=4 -> Y0=~x, z=1
            Y0 = 1 - x
            z = 1
        else:
            # Y0_z_unused: y>=5 -> Y0=x, z=0 (per candidate interpretation)
            Y0 = x
            z = 0
        results.append({"Y0": Y0, "z": z})
    return results
