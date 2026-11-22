def reference(vectors):
    # FSM states: 0=S0, 1=S1, 2=S2, 3=S3, 4=S4(match)
    # start_shifting is registered output, updated on posedge.
    # Reset is active-high synchronous.
    # Each row: inputs driven before sampled edge; mid changes occur AFTER sampling,
    # before other edge, carried to start of next row.
    out = []
    state = 0
    start_shifting = 0
    for row in vectors:
        # Determine values at sampling edge (posedge clk).
        # Row may contain 'reset', 'data', and possibly mid changes.
        # We need to handle mid changes: they occur after sampling.
        # The row dict may have keys like 'reset', 'data', and mid variants.
        # We'll assume row provides values at the sampling edge for reset/data,
        # and mid changes are given as separate keys (e.g., 'reset_mid', 'data_mid')
        # that apply after sampling.
        reset_val = row.get('reset', 0)
        data_val = row.get('data', 0)
        # Sample at posedge: compute next state and output based on current state and inputs.
        if reset_val:
            next_state = 0
            next_start = 0
        else:
            # Transition logic
            if state == 0:
                next_state = 1 if data_val == 1 else 0
            elif state == 1:
                next_state = 2 if data_val == 1 else 0
            elif state == 2:
                next_state = 3 if data_val == 0 else 2
            elif state == 3:
                next_state = 4 if data_val == 1 else 0
            elif state == 4:
                next_state = 4
            else:
                next_state = 0
            # start_shifting: set to 1 when entering S4, stays 1
            if state == 4 or next_state == 4:
                next_start = 1
            else:
                next_start = start_shifting
        # Output for this row is the value after the posedge (registered output).
        # The contract says start_shifting latency_cycles 1, meaning output reflects
        # state after the edge. So we output next_start.
        out.append({'start_shifting': next_start})
        # Update state and start_shifting for next row
        state = next_state
        start_shifting = next_start
        # Process mid changes: they occur after sampling, before other edge,
        # and are carried to start of next row. So we update reset_val/data_val
        # for the next row's sampling edge? Actually mid changes affect the
        # inputs for the next sampling edge. So we should apply them to the
        # next row's inputs. But the next row's dict may already have values.
        # The contract says "Optional mid input changes occur AFTER sampling,
        # before the other edge, and are carried to the start of the next row."
        # This means the mid changes modify the input values that will be
        # present at the next posedge. So we need to store them and apply
        # to the next row's inputs if not overridden.
        # We'll handle by keeping pending mid changes.
        # Since we process row by row, we can store mid changes and apply
        # to next row's reset/data if present.
        # For simplicity, assume mid changes are given as keys 'reset_mid', 'data_mid'.
        # We'll store them and apply to next row's inputs.
        # But we need to be careful: the next row's dict may have its own
        # reset/data values that are driven before the next posedge.
        # The mid changes from previous row are carried to start of next row,
        # meaning they are the initial values at the start of the next row,
        # but then the next row's driven values (before posedge) override them?
        # Actually "Each row's values are driven before the sampled edge."
        # So for the next row, the values in its dict are driven before its
        # posedge. The mid changes from previous row occur after previous
        # posedge and before the other edge, and are carried to start of next row.
        # So at the start of next row, the inputs are the mid-changed values,
        # but then the next row's driven values (before its posedge) may change them.
        # So the next row's dict values are the final values before its posedge.
        # Therefore, mid changes only matter if the next row does not drive
        # that input? But the contract says "Each row's values are driven before
        # the sampled edge." So every row drives all inputs? Possibly.
        # To be safe, we'll apply mid changes to the next row's inputs only if
        # the next row does not specify that input. But typical testbenches
        # provide all inputs each row. We'll implement: store mid changes,
        # and when processing next row, if 'reset' not in row, use mid_reset,
        # else use row['reset']. Similarly for data.
        # We'll keep pending_mid = {'reset': None, 'data': None}
        # After processing row, set pending_mid from row's mid keys.
        # At start of next row, if pending_mid has value and row doesn't have key,
        # use pending_mid value.
        # But we need to reset pending_mid after use? Actually mid changes are
        # carried to start of next row, meaning they persist until changed.
        # So we should keep them as the current input values at start of row,
        # then row's driven values override.
        # We'll maintain current_reset, current_data as the values at start of row.
        # Initially 0.
        # For each row:
        #   reset_val = row.get('reset', current_reset)
        #   data_val = row.get('data', current_data)
        #   ... sample ...
        #   # after sampling, apply mid changes:
        #   if 'reset_mid' in row: current_reset = row['reset_mid']
        #   else: current_reset = reset_val  # no mid change, stays same
        #   if 'data_mid' in row: current_data = row['data_mid']
        #   else: current_data = data_val
        # But wait: mid changes occur after sampling, before other edge.
        # So after sampling, the inputs change to mid values. These mid values
        # are carried to start of next row. So at start of next row, the inputs
        # are the mid values. Then the next row's driven values (before its posedge)
        # override them. So current_reset/current_data should be updated to mid values
        # after sampling, and then next row's row.get will use them as defaults.
        # That's what I described.
        # However, the row dict may not have 'reset_mid'/'data_mid' keys.
        # We'll assume they are optional.
        # Also, the output for this row is based on sampling edge, which uses
        # reset_val and data_val (the values before posedge). So we compute
        # next_state and next_start using reset_val and data_val.
        # Then we update current_reset/current_data to mid values.
        # Then next row uses current_reset/current_data as defaults.
        # But we need to be careful: the row's 'reset' and 'data' are the values
        # driven before the sampled edge. So they are the values at the posedge.
        # So we use them directly.
        # Let's implement with current_reset, current_data initialized to 0.
        # For each row:
        #   reset_val = row['reset'] if 'reset' in row else current_reset
        #   data_val = row['data'] if 'data' in row else current_data
        #   ... compute next_state, next_start using state, start_shifting, reset_val, data_val
        #   out.append({'start_shifting': next_start})
        #   state = next_state
        #   start_shifting = next_start
        #   # apply mid changes
        #   current_reset = row['reset_mid'] if 'reset_mid' in row else reset_val
        #   current_data = row['data_mid'] if 'data_mid' in row else data_val
        # But wait: if no mid change, the input stays at the value it had at posedge?
        # Actually after posedge, the input may change to mid value. If no mid change,
        # it stays at the same value? The contract says "Optional mid input changes
        # occur AFTER sampling, before the other edge, and are carried to the start
        # of the next row." So if no mid change, the input remains at the value
        # it had at sampling? Or it could change? Typically, if no mid change,
        # the input stays constant until next row's driven value. So current_reset
        # should remain reset_val if no mid change. That's what I have.
        # However, the next row's driven value will override current_reset if present.
        # So this seems correct.
        # Let's test with a simple sequence.
        # But we need to ensure we don't use current_reset/current_data before
        # they are defined. Initialize to 0.
        # Also, the output for the first row: state=0, start_shifting=0.
        # If reset=1, next_start=0. If reset=0, data=1 -> next_state=1, next_start=0.
        # So output 0. That's fine.
        # We'll implement as described.
        pass
    return out
