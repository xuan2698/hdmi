def reference(vectors):
    # Rule sync_reset_to_zero: If reset == 1 at the sampled posedge clk, q becomes 0.
    # Rule count_modulo_10: If reset == 0 at the sampled posedge clk, q becomes (previous q + 1) modulo 10.
    q = 0
    inputs = {"reset": 0}
    outputs = []
    for row in vectors:
        # Each row's values are driven before the sampled posedge.
        if "reset" in row:
            inputs["reset"] = row["reset"]

        # Synchronous update at posedge clk.
        if inputs["reset"] == 1:
            # sync_reset_to_zero
            q = 0
        else:
            # count_modulo_10
            if q == 9:
                q = 0
            else:
                q = q + 1

        outputs.append({"q": q})

        # Optional mid input changes occur AFTER sampling, before the other edge,
        # and are carried to the start of the next row.
        if "mid" in row:
            mid = row["mid"]
            if mid is not None:
                if "reset" in mid:
                    inputs["reset"] = mid["reset"]

    return outputs
