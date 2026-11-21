module audit(input wire [0:0] in_d, input wire [0:0] in_r, output wire [0:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_d;
reg [0:0] previous_r;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_d <= in_d;
previous_r <= in_r;
end
assign permit = (first || phase[0] || ((in_d == previous_d) && (in_r == previous_r))) && (!startup || ((in_r == 1)));
wire [0:0] gold_q;
wire [0:0] candidate_q;
cvdp_r_top_module gold_dut (.clk(phase[1]), .d(in_d), .r(in_r), .q(gold_q));
assign gold = {gold_q};
cvdp_m_top_module candidate_dut (.clk(phase[1]), .d(in_d), .r(in_r), .q(candidate_q));
assign candidate = {candidate_q};
endmodule
