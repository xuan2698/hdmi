def reference(vectors):
    history = 0
    result = []
    for row in vectors:
        if row["areset"]:
            history = 0
        elif row["train_mispredicted"]:
            history = ((row["train_history"] << 1) | row["train_taken"]) & 0xFFFFFFFF
        elif row["predict_valid"]:
            history = ((history << 1) | row["predict_taken"]) & 0xFFFFFFFF
        result.append({"predict_history": history & 0xFFFFFFFF})
    return result
