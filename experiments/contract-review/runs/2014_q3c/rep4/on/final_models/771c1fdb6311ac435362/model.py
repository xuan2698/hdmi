def reference(vectors):
    # Protocol: values driven before sampled edge; mid changes after sampling carry to next row.
    results = []
    cur_x = 0
    cur_y = 0
    for row in vectors:
        # Apply row values before the sampled edge.
        if "x" in row:
            cur_x = row["x"]
        if "y" in row:
            cur_y = row["y"]

        x = cur_x
        y = cur_y
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

        # Ensure concrete unsigned 1-bit outputs.
        Y0 = Y0 & 1
        z = z & 1
        results.append({"Y0": Y0, "z": z})

        # Process optional mid input changes AFTER sampling, before the other edge.
        if "mid" in row:
            mid = row["mid"]
            if "x" in mid:
                cur_x = mid["x"]
            if "y" in mid:
                cur_y = mid["y"]

    return results
