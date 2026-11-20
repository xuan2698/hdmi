def reference(vectors):
    # States: 0 = walk_left, 1 = walk_right, 2 = fall_left, 3 = fall_right
    state = 0  # after reset, walk left
    outputs = []
    for v in vectors:
        areset = v.get('areset', 0)
        bump_left = v.get('bump_left', 0)
        bump_right = v.get('bump_right', 0)
        ground = v.get('ground', 1)

        # Asynchronous reset (positive edge triggered) - if areset is 1, reset to walk_left
        if areset:
            state = 0
        else:
            if state == 0:  # walk_left
                if ground == 0:
                    state = 2  # fall_left
                elif bump_left or bump_right:
                    state = 1  # walk_right
            elif state == 1:  # walk_right
                if ground == 0:
                    state = 3  # fall_right
                elif bump_left or bump_right:
                    state = 0  # walk_left
            elif state == 2:  # fall_left
                if ground == 1:
                    state = 0  # resume walk_left
            elif state == 3:  # fall_right
                if ground == 1:
                    state = 1  # resume walk_right

        walk_left = 1 if state == 0 else 0
        walk_right = 1 if state == 1 else 0
        aaah = 1 if state in (2, 3) else 0
        outputs.append({'walk_left': walk_left, 'walk_right': walk_right, 'aaah': aaah})
    return outputs
