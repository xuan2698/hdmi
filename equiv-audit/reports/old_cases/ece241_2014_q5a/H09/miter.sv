module audit(input wire [0:0] in_areset, input wire [0:0] in_x, output wire [0:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_areset;
reg [0:0] previous_x;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_areset <= in_areset;
previous_x <= in_x;
end
assign permit = (first || phase[0] || ((in_areset == previous_areset) && (in_x == previous_x))) && (!startup || ((in_areset == 1)));
wire [0:0] gold_z;
wire [0:0] candidate_z;
cvdp_r_top_module gold_dut (.clk(phase[1]), .areset(in_areset), .x(in_x), .z(gold_z));
assign gold = {gold_z};
cvdp_m_top_module candidate_dut (.clk(phase[1]), .areset(in_areset), .x(in_x), .z(candidate_z));
assign candidate = {candidate_z};
endmodule
