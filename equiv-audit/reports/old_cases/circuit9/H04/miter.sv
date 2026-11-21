module audit(input wire [0:0] in_a, output wire [2:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_a;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_a <= in_a;
end
assign permit = (first || phase[0] || ((in_a == previous_a))) && (!startup || (1'b1));
wire [2:0] gold_q;
wire [2:0] candidate_q;
cvdp_r_top_module gold_dut (.clk(phase[1]), .a(in_a), .q(gold_q));
assign gold = {gold_q};
cvdp_m_top_module candidate_dut (.clk(phase[1]), .a(in_a), .q(candidate_q));
assign candidate = {candidate_q};
endmodule
