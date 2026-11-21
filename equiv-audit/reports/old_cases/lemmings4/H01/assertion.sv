module formal_top(input [0:0] in_areset, input [0:0] in_bump_left, input [0:0] in_bump_right, input [0:0] in_ground, input [0:0] in_dig);
wire [3:0] gold, candidate, gold_x, candidate_x;
wire [1:0] phase, phase_x;
wire permit, permit_x;
audit core (.in_areset(in_areset), .in_bump_left(in_bump_left), .in_bump_right(in_bump_right), .in_ground(in_ground), .in_dig(in_dig), .gold_d(gold), .candidate_d(candidate), .gold_x(gold_x),
    .candidate_x(candidate_x), .phase_d(phase), .phase_x(phase_x), .permit_d(permit), .permit_x(permit_x));
always @* begin
    assume (permit && !permit_x);
    assert ((((gold ^ candidate) | candidate_x) & ~gold_x) == 0);
end
endmodule
