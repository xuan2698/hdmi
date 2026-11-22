def reference(vectors):
    # Initial concrete power-up state: decimal count 0.
    count = 0
    outputs = []

    for row in vectors:
        reset = row.get('reset', 0)

        if reset:
            # Rule sync_active_high_reset: synchronous active-high reset
            # forces q=0 and ena=0 after the rising edge.
            count = 0
            q = 0
            ena = 0
        else:
            # Rule bcd_counter_increment: increment 4-digit BCD counter
            # modulo 10000 on a non-reset rising edge.
            count = (count + 1) % 10000

            ones = count % 10
            tens = (count // 10) % 10
            hundreds = (count // 100) % 10
            thousands = (count // 1000) % 10

            q = ones | (tens << 4) | (hundreds << 8) | (thousands << 12)

            # Rule upper_digit_enables: use the specified reversed bit order
            # interpretation: ena[2] = tens enable, ena[1] = hundreds enable,
            # ena[0] = thousands enable.
            ena = 0
            if ones == 9:
                ena |= 4  # ena[2]: tens should increment next
            if ones == 9 and tens == 9:
                ena |= 2  # ena[1]: hundreds should increment next
            if ones == 9 and tens == 9 and hundreds == 9:
                ena |= 1  # ena[0]: thousands should increment next

        outputs.append({'q': q, 'ena': ena})

    return outputs
