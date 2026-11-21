module audit(input wire [0:0] in_j, input wire [0:0] in_k, input wire [0:0] in_areset, output wire [0:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_j;
reg [0:0] previous_k;
reg [0:0] previous_areset;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_j <= in_j;
previous_k <= in_k;
previous_areset <= in_areset;
end
assign permit = (first || phase[0] || ((in_j == previous_j) && (in_k == previous_k) && (in_areset == previous_areset))) && (!startup || ((in_areset == 1)));
wire [0:0] gold_out;
wire [0:0] candidate_out;
cvdp_r_top_module gold_dut (.clk(phase[1]), .j(in_j), .k(in_k), .areset(in_areset), .out(gold_out));
assign gold = {gold_out};
cvdp_m_top_module candidate_dut (.clk(phase[1]), .j(in_j), .k(in_k), .areset(in_areset), .out(candidate_out));
assign candidate = {candidate_out};
endmodule
