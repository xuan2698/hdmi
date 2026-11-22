def reference(vectors):
    # Rule negedge_d_update and sync_reset_high: all DFFs triggered by negative edge of clk.
    # Rule sync_reset_high: active high synchronous reset. q reset to 0x34 (52) on negedge when reset==1.
    # Rule negedge_d_update: on negedge when reset==0, q captures d.
    q = 0
    cur_d = 0
    cur_reset = 0
    result = []
    for row in vectors:
        # Drive primary inputs before sampled negedge edge.
        if "d" in row:
            cur_d = row["d"]
        if "reset" in row:
            cur_reset = row["reset"]
        # Sample at negedge after edge settled.
        if cur_reset == 1:
            # Rule sync_reset_high implemented here.
            q = 52
        else:
            # Rule negedge_d_update implemented here.
            q = cur_d
        q = q & 0xFF  # keep within 8-bit output width
        result.append({"q": q})
        # Optional mid changes occur after sampling, before other edge, carried to next row.
        if "mid" in row:
            mid = row["mid"]
            try:
                if "d" in mid:
                    cur_d = mid["d"]
                if "reset" in mid:
                    cur_reset = mid["reset"]
            except:
                pass
        # Also support explicit _mid suffixed keys.
        if "d_mid" in row:
            cur_d = row["d_mid"]
        if "reset_mid" in row:
            cur_reset = row["reset_mid"]
    return result
