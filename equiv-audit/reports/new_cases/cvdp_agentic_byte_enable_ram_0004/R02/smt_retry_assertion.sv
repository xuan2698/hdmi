module formal_top(input [12:0] in_addr_a, input [0:0] in_en_a, input [3:0] in_be_a, input [31:0] in_data_in_a, input [12:0] in_addr_b, input [0:0] in_en_b, input [3:0] in_be_b, input [31:0] in_data_in_b);
wire [63:0] gold, candidate, gold_x, candidate_x;
wire [1:0] phase, phase_x;
wire permit, permit_x;
audit core (.in_addr_a(in_addr_a), .in_en_a(in_en_a), .in_be_a(in_be_a), .in_data_in_a(in_data_in_a), .in_addr_b(in_addr_b), .in_en_b(in_en_b), .in_be_b(in_be_b), .in_data_in_b(in_data_in_b), .gold_d(gold), .candidate_d(candidate), .gold_x(gold_x),
    .candidate_x(candidate_x), .phase_d(phase), .phase_x(phase_x), .permit_d(permit), .permit_x(permit_x));
always @* begin
    assume (permit && !permit_x && in_addr_a[12:1]==0 && in_addr_b[12:1]==0);
    assert ((((gold ^ candidate) | candidate_x) & ~gold_x) == 0);
end
endmodule
