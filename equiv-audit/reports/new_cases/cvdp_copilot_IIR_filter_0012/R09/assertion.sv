module formal_top(input [0:0] in_reset, input [15:0] in_in_1, input [15:0] in_in_2, input [15:0] in_in_3, input [1:0] in_filter_select);
wire [47:0] gold, candidate, gold_x, candidate_x;
wire [1:0] phase, phase_x;
wire permit, permit_x;
audit core (.in_reset(in_reset), .in_in_1(in_in_1), .in_in_2(in_in_2), .in_in_3(in_in_3), .in_filter_select(in_filter_select), .gold_d(gold), .candidate_d(candidate), .gold_x(gold_x),
    .candidate_x(candidate_x), .phase_d(phase), .phase_x(phase_x), .permit_d(permit), .permit_x(permit_x));
always @* begin
    assume (permit && !permit_x);
    assert ((((gold ^ candidate) | candidate_x) & ~gold_x) == 0);
end
endmodule
