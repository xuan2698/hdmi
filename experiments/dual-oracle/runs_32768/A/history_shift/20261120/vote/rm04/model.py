def reference(vectors):
    hist = 0
    mask = (1 << 32) - 1
    result = []

    for row in vectors:
        if int(row.get("areset", 0)) & 1:
            hist = 0
        elif int(row.get("train_mispredicted", 0)) & 1:
            train_history = int(row.get("train_history", 0)) & mask
            train_taken = int(row.get("train_taken", 0)) & 1
            hist = ((train_history << 1) | train_taken) & mask
        elif int(row.get("predict_valid", 0)) & 1:
            predict_taken = int(row.get("predict_taken", 0)) & 1
            hist = ((hist << 1) | predict_taken) & mask

        result.append({"predict_history": hist})

    return result
