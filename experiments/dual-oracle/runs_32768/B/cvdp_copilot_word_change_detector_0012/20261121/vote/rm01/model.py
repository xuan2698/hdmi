def reference(vectors):
    data_in_prev = 0
    latched_pattern = 0
    word_change_pulse = 0
    pattern_match_pulse = 0
    result = []
    for i, row in enumerate(vectors):
        reset = row.get('reset', 0)
        data_in = row.get('data_in', 0)
        mask = row.get('mask', 0)
        match_pattern = row.get('match_pattern', 0)
        enable = row.get('enable', 0)
        latch_pattern = row.get('latch_pattern', 0)

        if reset:
            data_in_prev = 0
            latched_pattern = 0
            word_change_pulse = 0
            pattern_match_pulse = 0

        result.append({
            'word_change_pulse': word_change_pulse,
            'pattern_match_pulse': pattern_match_pulse,
            'latched_pattern': latched_pattern
        })

        if i % 2 == 0 and not reset:
            old_latched = latched_pattern
            if enable:
                next_word = 1 if ((data_in ^ data_in_prev) & mask) != 0 else 0
                next_match = 1 if ((data_in & mask) == (old_latched & mask)) else 0
            else:
                next_word = 0
                next_match = 0

            if latch_pattern:
                latched_pattern = match_pattern

            word_change_pulse = next_word
            pattern_match_pulse = next_match
            data_in_prev = data_in

    return result
