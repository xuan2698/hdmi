module formal_top(input [0:0] in_reset, input [0:0] in_start, input [14:0] in_plaintext, input [44:0] in_key);
wire [15:0] gold, candidate, gold_x, candidate_x;
wire [1:0] phase, phase_x;
wire permit, permit_x;
audit core (.in_reset(in_reset), .in_start(in_start), .in_plaintext(in_plaintext), .in_key(in_key), .gold_d(gold), .candidate_d(candidate), .gold_x(gold_x),
    .candidate_x(candidate_x), .phase_d(phase), .phase_x(phase_x), .permit_d(permit), .permit_x(permit_x));
always @* begin
    assume (permit && !permit_x);
    assert ((((gold ^ candidate) | candidate_x) & ~gold_x) == 0);
end
endmodule
