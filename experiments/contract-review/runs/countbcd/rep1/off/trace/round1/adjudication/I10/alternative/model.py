def reference(vectors):
    # State: 4-digit BCD counter value
    # q[3:0]=ones, q[7:4]=tens, q[11:8]=hundreds, q[15:12]=thousands
    # Synchronous active-high reset.
    # Candidate interpretation for global: after reset deassert, counter holds q=0
    # for one cycle before first increment.
    #
    # We model: state q, and a flag "just_released" that is True on the cycle
    # immediately after reset deasserts (i.e., the first cycle with reset==0
    # following a cycle with reset==1). During that cycle, the counter holds
    # (does not increment). After that, normal increment behavior.
    #
    # Timing: outputs are sampled after posedge settles. Each row's inputs are
    # driven before the sampled edge. Mid changes occur AFTER sampling, before
    # the other edge, carried to start of next row. So for each row we:
    #   1. Apply any pending mid change to inputs (from previous row).
    #   2. Sample: compute outputs based on current state and current inputs
    #      (this is the value visible after the posedge for this row).
    #   3. Then compute next state based on current state and inputs (the
    #      posedge update), which becomes state for next row.
    #   4. Then apply this row's mid change (if any) to inputs for next row.
    #
    # Actually, the contract says: "Each row's values are driven before the
    # sampled edge. Optional mid input changes occur AFTER sampling, before the
    # other edge, and are carried to the start of the next row."
    #
    # So per row: inputs are set (including any carried mid change from prior
    # row). Then posedge occurs: outputs are sampled (visible same/next cycle
    # per rules), and state updates. Then mid change for this row is applied
    # (affects next row's inputs).
    #
    # The "visible" field: R1_reset visible same_cycle (reset forces q=0, ena=0
    # at the posedge). R2-R7 visible next_cycle: the increment happens at the
    # posedge, so the new q value is visible in the next cycle's sample.
    #
    # Wait — need to reconcile. The example for R1_reset:
    #   vectors: [{reset:1},{reset:0},{reset:0}]
    #   expected: [{q:0,ena:0},{q:1,ena:0},{q:2,ena:0}]
    # So at row 0 (reset=1), output q=0 (reset applied same cycle).
    # At row 1 (reset=0), output q=1 — meaning the counter incremented from 0
    # to 1 at the posedge of row 0? No — row 0 had reset=1, so state stays 0.
    # At row 1's posedge, reset=0, so counter increments 0->1, and output
    # visible at row 1 is q=1 (next_cycle visibility: the increment at row 1's
    # posedge is visible in row 1's sample? That contradicts "next_cycle").
    #
    # Let me re-read: "visible":"next_cycle" for R2. Example R2:
    #   vectors: [{reset:0},{reset:0},{reset:0}]
    #   expected: [{q:1,ena:0},{q:2,ena:0},{q:3,ena:0}]
    # So starting from q=0 (power-up unspecified but presumably 0), at row 0
    # posedge the counter increments to 1, and row 0's output is q=1. That's
    # "same cycle" visibility actually — the increment at this posedge is
    # reflected in this row's output. Hmm, but they call it next_cycle.
    #
    # Actually the convention here: the output sampled after the posedge
    # reflects the new state (post-edge). So "next_cycle" means the value
    # after the edge, which is what we sample. The example confirms: row 0
    # output q=1 means after row 0's posedge, q=1.
    #
    # For R1_reset example: row 0 reset=1, output q=0 (reset applied at edge,
    # post-edge q=0). Row 1 reset=0, output q=1 (post-edge q=1, incremented
    # from 0). Row 2 reset=0, output q=2. Consistent: output = post-edge state.
    #
    # So the model is simple: for each row, compute the post-posedge state
    # (applying reset or increment), and that post-edge state is the output
    # for that row. ena is also computed from the pre-edge state (the state
    # that determines whether upper digits increment at this edge).
    #
    # Check R4_ena_tens example:
    #   vectors: [{reset:0},{reset:0},{reset:0}]
    #   expected: [{q:9,ena:1},{q:10,ena:0},{q:11,ena:0}]
    # Row 0: pre-edge q=8 (assumed), ones=8 !=9, so no carry, post-edge q=9.
    #   But ena=1 at row 0? That means ena reflects the carry condition at
    #   this edge: ones==9 pre-edge? If pre-edge q=8, ones=8, no carry.
    #   Hmm. Let's think: maybe pre-edge q=9? Then post-edge q would be 10,
    #   not 9. Contradiction.
    #
    # Alternative: ena is computed from the post-edge state? Post-edge q=9,
    # ones=9, so ena_tens=1 (indicating tens should increment next). That
    # matches! Row 1: post-edge q=10, ones=0, ena=0. Row 2: post-edge q=11,
    # ones=1, ena=0. Yes!
    #
    # Check R5_ena_hundreds example:
    #   expected: [{q:99,ena:3},{q:100,ena:0},{q:101,ena:0}]
    # Row 0 post-edge q=99: ones=9 -> ena_tens=1; ones=9 and tens=9 ->
    #   ena_hundreds=1. ena=3 (bits: ena[0]=tens, ena[1]=hundreds,
    #   ena[2]=thousands). So ena=0b011=3. Matches.
    # Row 1 post-edge q=100: ones=0, ena=0. Matches.
    #
    # Check R6_ena_thousands example:
    #   expected: [{q:999,ena:7},{q:1000,ena:0},{q:1001,ena:0}]
    # Row 0 post-edge q=999: ones=9,tens=9,hundreds=9 -> ena=0b111=7. Matches.
    #
    # So: ena is computed from the POST-edge state q (the output q for this
    # row). ena[0] = (ones==9), ena[1] = (ones==9 and tens==9),
    # ena[2] = (ones==9 and tens==9 and hundreds==9).
    #
    # And q output = post-edge state.
    #
    # Now the global candidate interpretation: "After reset deassert, counter
    # holds q=0 for one cycle before first increment."
    #
    # So: when reset goes from 1 to 0, the first cycle with reset=0 does NOT
    # increment; it holds at 0. Then subsequent cycles increment normally.
    #
    # Let's verify against R1_reset example:
    #   vectors: [{reset:1},{reset:0},{reset:0}]
    #   expected: [{q:0,ena:0},{q:1,ena:0},{q:2,ena:0}]
    # Row 0: reset=1, post-edge q=0.
    # Row 1: reset=0, first cycle after deassert -> hold q=0? But expected
    #   q=1. Contradiction with the candidate interpretation!
    #
    # Hmm. The candidate interpretation says "holds q=0 for one cycle before
    # first increment". But the R1 example shows q=1 at row 1 (first cycle
    # after deassert). So the candidate interpretation conflicts with the
    # example.
    #
    # The instructions say: "For the listed unresolved fields apply these
    # candidate interpretations instead". The unresolved field is R7_full_wrap
    # (uncertain), but the candidate interpretation given is for "global".
    # The global interpretation is about post-reset behavior.
    #
    # Given the conflict, I should follow the candidate interpretation as
    # instructed, since it's explicitly given as the interpretation to apply.
    # But the example in R1_reset is part of the contract... The instructions
    # say "For the listed unresolved fields apply these candidate
    # interpretations instead" — meaning override the contract where the
    # candidate applies. The global candidate applies to post-reset behavior.
    #
    # However, the R1 example is a concrete expected output. If I apply the
    # hold-one-cycle interpretation, row 1 would be q=0, not q=1, violating
    # the example. But the example might be illustrative of the general rule
    # without the candidate interpretation applied.
    #
    # I'll follow the candidate interpretation as instructed: after reset
    # deassert, hold q=0 for one cycle, then increment.
    #
    # So state machine:
    #   - reset=1: q=0, just_released=False (or set a flag)
    #   - reset=0 and just_released: q holds (stays 0), just_released=False
    #   - reset=0 and not just_released: normal BCD increment
    #
    # When does just_released become True? On the posedge where reset
    # transitions from 1 to 0. So we need to track previous reset value.
    #
    # Let's define: prev_reset (reset value from previous row's posedge).
    # At each posedge:
    #   if reset==1: q=0, hold_flag=False
    #   elif prev_reset==1 (just deasserted): q holds (q stays), hold_flag=False
    #   else: normal increment
    #   prev_reset = reset
    #
    # Wait, but "holds q=0 for one cycle" — if q was 0 from reset, holding
    # means q stays 0. So row 1 (first reset=0) would output q=0. Row 2
    # would increment to 1. This contradicts R1 example but follows the
    # candidate interpretation.
    #
    # Actually, let me reconsider. The candidate interpretation might be
    # describing the behavior when reset is deasserted and the counter is at
    # 0 — it holds at 0 for one cycle. But the R1 example shows q=1 at the
    # first reset=0 cycle. These are contradictory.
    #
    # Given the explicit instruction to apply the candidate interpretation,
    # I'll implement the hold-one-cycle behavior. The R1 example may be
    # from the original spec without the candidate applied.
    #
    # Hmm, but actually re-reading: "For the listed unresolved fields apply
    # these candidate interpretations instead". The listed unresolved field
    # is R7_full_wrap. The candidate interpretation given is for "global".
    # This is a bit ambiguous. The global interpretation is about post-reset
    # behavior, which is a different aspect than R7.
    #
    # I think the safest reading: the candidate interpretation for "global"
    # is the one to apply. It says: after reset deassert, hold q=0 for one
    # cycle before first increment.
    #
    # Let me implement that.
    #
    # Also need to handle R7_full_wrap: wrap to 0000 (first candidate).
    #
    # BCD increment logic:
    #   ones = q & 0xF
    #   tens = (q >> 4) & 0xF
    #   hundreds = (q >> 8) & 0xF
    #   thousands = (q >> 12) & 0xF
    #   if ones != 9: ones += 1
    #   else: ones = 0; if tens != 9: tens += 1
    #         else: tens = 0; if hundreds != 9: hundreds += 1
    #               else: hundreds = 0; if thousands != 9: thousands += 1
    #                     else: thousands = 0  (wrap)
    #
    # ena computed from post-edge q:
    #   ena[0] = 1 if ones==9 else 0
    #   ena[1] = 1 if ones==9 and tens==9 else 0
    #   ena[2] = 1 if ones==9 and tens==9 and hundreds==9 else 0

    q = 0
    prev_reset = 0  # power-up: assume reset not previously asserted
    # Actually power-up state is unspecified; we start with q=0, prev_reset=0.
    # The first row's reset value determines behavior.

    results = []
    for row in vectors:
        reset = row.get('reset', 0)

        # Determine post-edge state
        if reset == 1:
            # R1_reset: synchronous active-high reset -> q=0
            new_q = 0
        elif prev_reset == 1:
            # Global candidate: after reset deassert, hold q for one cycle
            new_q = q
        else:
            # Normal BCD increment
            ones = q & 0xF
            tens = (q >> 4) & 0xF
            hundreds = (q >> 8) & 0xF
            thousands = (q >> 12) & 0xF
            if ones != 9:
                ones += 1
            else:
                ones = 0
                if tens != 9:
                    tens += 1
                else:
                    tens = 0
                    if hundreds != 9:
                        hundreds += 1
                    else:
                        hundreds = 0
                        if thousands != 9:
                            thousands += 1
                        else:
                            thousands = 0  # R7_full_wrap: wrap to 0000
            new_q = ones | (tens << 4) | (hundreds << 8) | (thousands << 12)

        # Output q is post-edge state
        out_q = new_q

        # ena computed from post-edge q
        ones = out_q & 0xF
        tens = (out_q >> 4) & 0xF
        hundreds = (out_q >> 8) & 0xF
        ena_tens = 1 if ones == 9 else 0
        ena_hundreds = 1 if (ones == 9 and tens == 9) else 0
        ena_thousands = 1 if (ones == 9 and tens == 9 and hundreds == 9) else 0
        out_ena = ena_tens | (ena_hundreds << 1) | (ena_thousands << 2)

        results.append({'q': out_q, 'ena': out_ena})

        # Update state for next row
        q = new_q
        prev_reset = reset

    return results
