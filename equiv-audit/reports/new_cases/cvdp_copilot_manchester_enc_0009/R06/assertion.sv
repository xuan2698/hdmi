module formal_top(input [0:0] in_rst_in, input [0:0] in_enc_valid_in, input [7:0] in_enc_data_in, input [0:0] in_dec_valid_in, input [15:0] in_dec_data_in);
wire [25:0] gold, candidate, gold_x, candidate_x;
wire [1:0] phase, phase_x;
wire permit, permit_x;
audit core (.in_rst_in(in_rst_in), .in_enc_valid_in(in_enc_valid_in), .in_enc_data_in(in_enc_data_in), .in_dec_valid_in(in_dec_valid_in), .in_dec_data_in(in_dec_data_in), .gold_d(gold), .candidate_d(candidate), .gold_x(gold_x),
    .candidate_x(candidate_x), .phase_d(phase), .phase_x(phase_x), .permit_d(permit), .permit_x(permit_x));
always @* begin
    assume (permit && !permit_x);
    assert ((((gold ^ candidate) | candidate_x) & ~gold_x) == 0);
end
endmodule
