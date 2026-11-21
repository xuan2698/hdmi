module audit(input wire [0:0] in_areset, input wire [0:0] in_bump_left, input wire [0:0] in_bump_right, input wire [0:0] in_ground, output wire [2:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_areset;
reg [0:0] previous_bump_left;
reg [0:0] previous_bump_right;
reg [0:0] previous_ground;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_areset <= in_areset;
previous_bump_left <= in_bump_left;
previous_bump_right <= in_bump_right;
previous_ground <= in_ground;
end
assign permit = (first || phase[0] || ((in_areset == previous_areset) && (in_bump_left == previous_bump_left) && (in_bump_right == previous_bump_right) && (in_ground == previous_ground))) && (!startup || ((in_areset == 1)));
wire [0:0] gold_walk_left;
wire [0:0] gold_walk_right;
wire [0:0] gold_aaah;
wire [0:0] candidate_walk_left;
wire [0:0] candidate_walk_right;
wire [0:0] candidate_aaah;
cvdp_r_top_module gold_dut (.clk(phase[1]), .areset(in_areset), .bump_left(in_bump_left), .bump_right(in_bump_right), .ground(in_ground), .walk_left(gold_walk_left), .walk_right(gold_walk_right), .aaah(gold_aaah));
assign gold = {gold_walk_left, gold_walk_right, gold_aaah};
cvdp_m_top_module candidate_dut (.clk(phase[1]), .areset(in_areset), .bump_left(in_bump_left), .bump_right(in_bump_right), .ground(in_ground), .walk_left(candidate_walk_left), .walk_right(candidate_walk_right), .aaah(candidate_aaah));
assign candidate = {candidate_walk_left, candidate_walk_right, candidate_aaah};
endmodule
