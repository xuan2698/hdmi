module formal_top(input [0:0] in_load, input [0:0] in_ena, input [1:0] in_amount, input [63:0] in_data);
wire [63:0] gold, candidate, gold_x, candidate_x;
wire [1:0] phase, phase_x;
wire permit, permit_x;
audit core (.in_load(in_load), .in_ena(in_ena), .in_amount(in_amount), .in_data(in_data), .gold_d(gold), .candidate_d(candidate), .gold_x(gold_x),
    .candidate_x(candidate_x), .phase_d(phase), .phase_x(phase_x), .permit_d(permit), .permit_x(permit_x));
always @* begin
    assume (permit && !permit_x);
    assert ((((gold ^ candidate) | candidate_x) & ~gold_x) == 0);
end
endmodule
