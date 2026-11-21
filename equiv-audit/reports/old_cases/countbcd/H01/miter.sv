module audit(input wire [0:0] in_reset, output wire [18:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_reset;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_reset <= in_reset;
end
assign permit = (first || phase[0] || ((in_reset == previous_reset))) && (!startup || ((in_reset == 1)));
wire [2:0] gold_ena;
wire [15:0] gold_q;
wire [2:0] candidate_ena;
wire [15:0] candidate_q;
cvdp_r_top_module gold_dut (.clk(phase[1]), .reset(in_reset), .ena(gold_ena), .q(gold_q));
assign gold = {gold_ena, gold_q};
cvdp_m_top_module candidate_dut (.clk(phase[1]), .reset(in_reset), .ena(candidate_ena), .q(candidate_q));
assign candidate = {candidate_ena, candidate_q};
endmodule
