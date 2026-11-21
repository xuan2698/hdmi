module formal_top(input [0:0] in_reset, input [7:0] in_data_in, input [7:0] in_mask, input [7:0] in_match_pattern, input [0:0] in_enable, input [0:0] in_latch_pattern);
wire [9:0] gold, candidate, gold_x, candidate_x;
wire [1:0] phase, phase_x;
wire permit, permit_x;
audit core (.in_reset(in_reset), .in_data_in(in_data_in), .in_mask(in_mask), .in_match_pattern(in_match_pattern), .in_enable(in_enable), .in_latch_pattern(in_latch_pattern), .gold_d(gold), .candidate_d(candidate), .gold_x(gold_x),
    .candidate_x(candidate_x), .phase_d(phase), .phase_x(phase_x), .permit_d(permit), .permit_x(permit_x));
always @* begin
    assume (permit && !permit_x);
    assert ((((gold ^ candidate) | candidate_x) & ~gold_x) == 0);
end
endmodule
