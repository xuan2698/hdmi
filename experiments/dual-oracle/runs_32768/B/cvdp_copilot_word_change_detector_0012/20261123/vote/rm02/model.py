def reference(vectors):
    W = 8
    ALL = (1 << W) - 1

    def getv(row, names, default=0):
        for n in names:
            if n in row:
                return row[n]
        for k in row:
            if isinstance(k, str):
                lk = k.lower()
                for n in names:
                    if lk == n.lower():
                        return row[k]
        return default

    def as_int(x):
        if isinstance(x, str):
            try:
                return int(x, 0)
            except:
                try:
                    return int(x)
                except:
                    return 0
        try:
            return int(x)
        except:
            return 0

    word_change_pulse = 0
    pattern_match_pulse = 0
    latched_pattern = 0
    data_in_prev = 0

    result = []

    for row in vectors:
        e = getv(row, ['edge'], None)
        if e is None:
            clk = getv(row, ['clk'], None)
            if clk is not None:
                e = 1 if as_int(clk) else 0

        if isinstance(e, str):
            es = e.lower()
            is_posedge = ('pos' in es) or ('rise' in es) or (es in ('1', 'p', 'true'))
            if ('neg' in es) or ('fall' in es) or (es in ('0', 'n', 'false')):
                is_posedge = False
        else:
            if e is None:
                is_posedge = True
            else:
                is_posedge = bool(as_int(e))

        reset = as_int(getv(row, ['reset'], 0)) != 0

        if reset:
            word_change_pulse = 0
            pattern_match_pulse = 0
            latched_pattern = 0
            data_in_prev = 0

        result.append({
            'word_change_pulse': word_change_pulse,
            'pattern_match_pulse': pattern_match_pulse,
            'latched_pattern': latched_pattern
        })

        if is_posedge:
            if reset:
                word_change_pulse = 0
                pattern_match_pulse = 0
                latched_pattern = 0
                data_in_prev = 0
            else:
                data_in = as_int(getv(row, ['data_in'], 0)) & ALL
                mask = as_int(getv(row, ['mask'], 0)) & ALL
                match_pattern = as_int(getv(row, ['match_pattern'], 0)) & ALL
                enable = as_int(getv(row, ['enable'], 0)) != 0
                latch_pattern = as_int(getv(row, ['latch_pattern'], 0)) != 0

                changed = enable and (((data_in ^ data_in_prev) & mask) != 0)
                matched = enable and ((data_in & mask) == (latched_pattern & mask))

                word_change_pulse = 1 if changed else 0
                pattern_match_pulse = 1 if matched else 0

                if latch_pattern:
                    latched_pattern = match_pattern

                data_in_prev = data_in

    return result
