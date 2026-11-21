module audit(input wire [0:0] in_reset, output wire [6:0] gold, candidate, output wire [1:0] phase, output wire permit);
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
wire [0:0] gold_release_reset_o;
wire [0:0] gold_gate_clk_o;
wire [4:0] gold_cnt_q;
wire [0:0] candidate_release_reset_o;
wire [0:0] candidate_gate_clk_o;
wire [4:0] candidate_cnt_q;
cvdp_r_async_reset gold_dut (.clk(phase[1]), .reset(in_reset), .release_reset_o(gold_release_reset_o), .gate_clk_o(gold_gate_clk_o), .cnt_q(gold_cnt_q));
assign gold = {gold_release_reset_o, gold_gate_clk_o, gold_cnt_q};
cvdp_m_async_reset candidate_dut (.clk(phase[1]), .reset(in_reset), .release_reset_o(candidate_release_reset_o), .gate_clk_o(candidate_gate_clk_o), .cnt_q(candidate_cnt_q));
assign candidate = {candidate_release_reset_o, candidate_gate_clk_o, candidate_cnt_q};
endmodule
