module audit(input wire [0:0] in_reset, input wire [0:0] in_data, output wire [0:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_reset;
reg [0:0] previous_data;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_reset <= in_reset;
previous_data <= in_data;
end
assign permit = (first || phase[0] || ((in_reset == previous_reset) && (in_data == previous_data))) && (!startup || ((in_reset == 1)));
wire [0:0] gold_start_shifting;
wire [0:0] candidate_start_shifting;
cvdp_r_top_module gold_dut (.clk(phase[1]), .reset(in_reset), .data(in_data), .start_shifting(gold_start_shifting));
assign gold = {gold_start_shifting};
cvdp_m_top_module candidate_dut (.clk(phase[1]), .reset(in_reset), .data(in_data), .start_shifting(candidate_start_shifting));
assign candidate = {candidate_start_shifting};
endmodule
