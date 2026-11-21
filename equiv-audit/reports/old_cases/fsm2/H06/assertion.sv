module formal_top(input [0:0] in_j, input [0:0] in_k, input [0:0] in_areset);
wire [0:0] gold, candidate, gold_x, candidate_x;
wire [1:0] phase, phase_x;
wire permit, permit_x;
audit core (.in_j(in_j), .in_k(in_k), .in_areset(in_areset), .gold_d(gold), .candidate_d(candidate), .gold_x(gold_x),
    .candidate_x(candidate_x), .phase_d(phase), .phase_x(phase_x), .permit_d(permit), .permit_x(permit_x));
always @* begin
    assume (permit && !permit_x);
    assert ((((gold ^ candidate) | candidate_x) & ~gold_x) == 0);
end
endmodule
