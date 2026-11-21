module formal_top(input [0:0] in_rst, input [3:0] in_data_in, input [0:0] in_has_data_to_send);
wire [11:0] gold, candidate, gold_x, candidate_x;
wire [1:0] phase, phase_x;
wire permit, permit_x;
audit core (.in_rst(in_rst), .in_data_in(in_data_in), .in_has_data_to_send(in_has_data_to_send), .gold_d(gold), .candidate_d(candidate), .gold_x(gold_x),
    .candidate_x(candidate_x), .phase_d(phase), .phase_x(phase_x), .permit_d(permit), .permit_x(permit_x));
always @* begin
    assume (permit && !permit_x);
    assert ((((gold ^ candidate) | candidate_x) & ~gold_x) == 0);
end
endmodule
