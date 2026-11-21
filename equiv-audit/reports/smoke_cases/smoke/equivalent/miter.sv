module audit(input wire [0:0] in_x, output wire [0:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_x;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_x <= in_x;
end
assign permit = (first || phase[0] || ((in_x == previous_x))) && (!startup || (1'b1));
wire [0:0] gold_q;
wire [0:0] candidate_q;
cvdp_r_probe gold_dut (.clk(phase[1]), .x(in_x), .q(gold_q));
assign gold = {gold_q};
cvdp_m_probe candidate_dut (.clk(phase[1]), .x(in_x), .q(candidate_q));
assign candidate = {candidate_q};
endmodule
