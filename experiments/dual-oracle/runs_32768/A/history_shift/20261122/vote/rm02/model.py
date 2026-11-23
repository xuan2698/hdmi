def reference(vectors):
    h = 0
    out = []
    for v in vectors:
        if v.get("areset", 0):
            h = 0
        elif v.get("train_mispredicted", 0):
            h = (((v.get("train_history", 0) & 0x7fffffff) << 1) | (v.get("train_taken", 0) & 1)) & 0xffffffff
        elif v.get("predict_valid", 0):
            h = (((h & 0x7fffffff) << 1) | (v.get("predict_taken", 0) & 1)) & 0xffffffff
        out.append({"predict_history": h})
    return out
