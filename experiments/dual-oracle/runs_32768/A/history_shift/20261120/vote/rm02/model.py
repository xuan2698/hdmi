def reference(vectors):
    h = 0
    r = []
    for v in vectors:
        if v.get('areset', 0):
            h = 0
        elif v.get('train_mispredicted', 0):
            th = v.get('train_history', 0) & 0xffffffff
            tt = v.get('train_taken', 0) & 1
            h = ((th << 1) & 0xffffffff) | tt
        elif v.get('predict_valid', 0):
            pt = v.get('predict_taken', 0) & 1
            h = ((h << 1) & 0xffffffff) | pt
        r.append({'predict_history': h & 0xffffffff})
    return r
