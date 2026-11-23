def reference(vectors):
    q = 0
    m = (1 << 32) - 1
    keys = ['areset', 'predict_valid', 'predict_taken', 'train_mispredicted', 'train_taken', 'train_history']
    cur = {k: 0 for k in keys}
    out = []
    for row in vectors:
        for k, v in row.items():
            if k != 'mid':
                cur[k] = v
        if cur.get('areset', 0):
            q = 0
        elif cur.get('train_mispredicted', 0):
            q = ((cur.get('train_history', 0) << 1) | cur.get('train_taken', 0)) & m
        elif cur.get('predict_valid', 0):
            q = ((q << 1) | cur.get('predict_taken', 0)) & m
        q &= m
        out.append({'predict_history': q})
        mid = row.get('mid')
        if mid:
            for k, v in mid.items():
                cur[k] = v
            if cur.get('areset', 0):
                q = 0
    return out
