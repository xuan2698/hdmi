module audit(input wire [0:0] in_reset, input wire [0:0] in_ena, output wire [24:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_reset;
reg [0:0] previous_ena;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_reset <= in_reset;
previous_ena <= in_ena;
end
assign permit = (first || phase[0] || ((in_reset == previous_reset) && (in_ena == previous_ena))) && (!startup || ((in_reset == 1)));
wire [0:0] gold_pm;
wire [7:0] gold_hh;
wire [7:0] gold_mm;
wire [7:0] gold_ss;
wire [0:0] candidate_pm;
wire [7:0] candidate_hh;
wire [7:0] candidate_mm;
wire [7:0] candidate_ss;
cvdp_r_top_module gold_dut (.clk(phase[1]), .reset(in_reset), .ena(in_ena), .pm(gold_pm), .hh(gold_hh), .mm(gold_mm), .ss(gold_ss));
assign gold = {gold_pm, gold_hh, gold_mm, gold_ss};
cvdp_m_top_module candidate_dut (.clk(phase[1]), .reset(in_reset), .ena(in_ena), .pm(candidate_pm), .hh(candidate_hh), .mm(candidate_mm), .ss(candidate_ss));
assign candidate = {candidate_pm, candidate_hh, candidate_mm, candidate_ss};
endmodule
