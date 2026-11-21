module audit(input wire [0:0] in_x, input wire [2:0] in_y, output wire [1:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_x;
reg [2:0] previous_y;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_x <= in_x;
previous_y <= in_y;
end
assign permit = (first || phase[0] || ((in_x == previous_x) && (in_y == previous_y))) && (!startup || (1'b1));
wire [0:0] gold_Y0;
wire [0:0] gold_z;
wire [0:0] candidate_Y0;
wire [0:0] candidate_z;
cvdp_r_top_module gold_dut (.clk(phase[1]), .x(in_x), .y(in_y), .Y0(gold_Y0), .z(gold_z));
assign gold = {gold_Y0, gold_z};
cvdp_m_top_module candidate_dut (.clk(phase[1]), .x(in_x), .y(in_y), .Y0(candidate_Y0), .z(candidate_z));
assign candidate = {candidate_Y0, candidate_z};
endmodule
