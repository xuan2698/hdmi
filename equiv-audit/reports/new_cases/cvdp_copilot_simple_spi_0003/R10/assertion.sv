module formal_top(input [0:0] in_i_rst_b, input [15:0] in_i_data_in, input [0:0] in_i_enable, input [0:0] in_i_fault, input [0:0] in_i_clear);
wire [10:0] gold, candidate, gold_x, candidate_x;
wire [1:0] phase, phase_x;
wire permit, permit_x;
audit core (.in_i_rst_b(in_i_rst_b), .in_i_data_in(in_i_data_in), .in_i_enable(in_i_enable), .in_i_fault(in_i_fault), .in_i_clear(in_i_clear), .gold_d(gold), .candidate_d(candidate), .gold_x(gold_x),
    .candidate_x(candidate_x), .phase_d(phase), .phase_x(phase_x), .permit_d(permit), .permit_x(permit_x));
always @* begin
    assume (permit && !permit_x);
    assert ((((gold ^ candidate) | candidate_x) & ~gold_x) == 0);
end
endmodule
