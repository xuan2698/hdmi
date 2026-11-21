module audit(input wire [0:0] in_load, input wire [511:0] in_data, output wire [511:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_load;
reg [511:0] previous_data;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_load <= in_load;
previous_data <= in_data;
end
assign permit = (first || phase[0] || ((in_load == previous_load) && (in_data == previous_data))) && (!startup || (1'b1));
wire [511:0] gold_q;
wire [511:0] candidate_q;
cvdp_r_top_module gold_dut (.clk(phase[1]), .load(in_load), .data(in_data), .q(gold_q));
assign gold = {gold_q};
cvdp_m_top_module candidate_dut (.clk(phase[1]), .load(in_load), .data(in_data), .q(candidate_q));
assign candidate = {candidate_q};
endmodule
