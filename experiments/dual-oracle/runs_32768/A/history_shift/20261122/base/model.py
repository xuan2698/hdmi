def reference(vectors):
    s = 0
    M = 0xffffffff
    i = {'areset': 0, 'predict_valid': 0, 'predict_taken': 0, 'train_mispredicted': 0, 'train_taken': 0, 'train_history': 0}
    o = []
    for r in vectors:
        for k, v in r.items():
            if k != 'mid':
                i[k] = v
        if i['areset']:
            s = 0
        elif i['train_mispredicted']:
            s = ((((i['train_history'] & M) << 1) & M) | (i['train_taken'] & 1)) & M
        elif i['predict_valid']:
            s = (((s << 1) & M) | (i['predict_taken'] & 1)) & M
        o.append({'predict_history': s & M})
        for k, v in r.get('mid', {}).items():
            i[k] = v
        if i['areset']:
            s = 0
    return o
