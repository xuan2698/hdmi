def reference(vectors):
    state = 'WALK_LEFT'
    fall_count = 0
    out = []
    for v in vectors:
        areset = v['areset']
        bump_left = v['bump_left']
        bump_right = v['bump_right']
        ground = v['ground']
        dig = v['dig']
        if areset:
            state = 'WALK_LEFT'
            fall_count = 0
        if state == 'WALK_LEFT':
            o = {'walk_left':1,'walk_right':0,'aaah':0,'digging':0}
        elif state == 'WALK_RIGHT':
            o = {'walk_left':0,'walk_right':1,'aaah':0,'digging':0}
        elif state in ('FALL_LEFT','FALL_RIGHT'):
            o = {'walk_left':0,'walk_right':0,'aaah':1,'digging':0}
        elif state in ('DIG_LEFT','DIG_RIGHT'):
            o = {'walk_left':0,'walk_right':0,'aaah':0,'digging':1}
        else:
            o = {'walk_left':0,'walk_right':0,'aaah':0,'digging':0}
        out.append(o)
        if areset:
            continue
        if state == 'WALK_LEFT':
            if ground == 0:
                state = 'FALL_LEFT'
                fall_count = 0
            elif dig == 1:
                state = 'DIG_LEFT'
            elif bump_left or bump_right:
                state = 'WALK_RIGHT'
        elif state == 'WALK_RIGHT':
            if ground == 0:
                state = 'FALL_RIGHT'
                fall_count = 0
            elif dig == 1:
                state = 'DIG_RIGHT'
            elif bump_left or bump_right:
                state = 'WALK_LEFT'
        elif state == 'FALL_LEFT':
            if ground == 1:
                if fall_count > 20:
                    state = 'SPLAT'
                else:
                    state = 'WALK_LEFT'
                fall_count = 0
            else:
                fall_count += 1
        elif state == 'FALL_RIGHT':
            if ground == 1:
                if fall_count > 20:
                    state = 'SPLAT'
                else:
                    state = 'WALK_RIGHT'
                fall_count = 0
            else:
                fall_count += 1
        elif state == 'DIG_LEFT':
            if ground == 0:
                state = 'FALL_LEFT'
                fall_count = 0
        elif state == 'DIG_RIGHT':
            if ground == 0:
                state = 'FALL_RIGHT'
                fall_count = 0
        elif state == 'SPLAT':
            pass
    return out
