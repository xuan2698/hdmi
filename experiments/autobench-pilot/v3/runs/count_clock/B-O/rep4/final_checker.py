def reference(vectors):
    state = {'hh': 12, 'mm': 0, 'ss': 0, 'pm': 0}
    out = []
    def tick(s):
        s['ss'] += 1
        if s['ss'] == 60:
            s['ss'] = 0
            s['mm'] += 1
            if s['mm'] == 60:
                s['mm'] = 0
                s['hh'] += 1
                if s['hh'] == 13:
                    s['hh'] = 1
                    s['pm'] ^= 1
                elif s['hh'] == 12:
                    s['pm'] ^= 1
    for row in vectors:
        if row.get('reset'):
            state['hh'], state['mm'], state['ss'], state['pm'] = 12, 0, 0, 0
        elif row.get('ena'):
            tick(state)
        out.append({'pm': state['pm'],
                    'hh': ((state['hh'] // 10) << 4) | (state['hh'] % 10),
                    'mm': ((state['mm'] // 10) << 4) | (state['mm'] % 10),
                    'ss': ((state['ss'] // 10) << 4) | (state['ss'] % 10)})
        if 'mid' in row:
            m = row['mid']
            if m.get('reset'):
                state['hh'], state['mm'], state['ss'], state['pm'] = 12, 0, 0, 0
            elif m.get('ena'):
                tick(state)
    return out
