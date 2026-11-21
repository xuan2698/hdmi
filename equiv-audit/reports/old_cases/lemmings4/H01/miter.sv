module audit(input wire [0:0] in_areset, input wire [0:0] in_bump_left, input wire [0:0] in_bump_right, input wire [0:0] in_ground, input wire [0:0] in_dig, output wire [3:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_areset;
reg [0:0] previous_bump_left;
reg [0:0] previous_bump_right;
reg [0:0] previous_ground;
reg [0:0] previous_dig;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_areset <= in_areset;
previous_bump_left <= in_bump_left;
previous_bump_right <= in_bump_right;
previous_ground <= in_ground;
previous_dig <= in_dig;
end
assign permit = (first || phase[0] || ((in_areset == previous_areset) && (in_bump_left == previous_bump_left) && (in_bump_right == previous_bump_right) && (in_ground == previous_ground) && (in_dig == previous_dig))) && (!startup || ((in_areset == 1)));
wire [0:0] gold_walk_left;
wire [0:0] gold_walk_right;
wire [0:0] gold_aaah;
wire [0:0] gold_digging;
wire [0:0] candidate_walk_left;
wire [0:0] candidate_walk_right;
wire [0:0] candidate_aaah;
wire [0:0] candidate_digging;
cvdp_r_top_module gold_dut (.clk(phase[1]), .areset(in_areset), .bump_left(in_bump_left), .bump_right(in_bump_right), .ground(in_ground), .dig(in_dig), .walk_left(gold_walk_left), .walk_right(gold_walk_right), .aaah(gold_aaah), .digging(gold_digging));
assign gold = {gold_walk_left, gold_walk_right, gold_aaah, gold_digging};
cvdp_m_top_module candidate_dut (.clk(phase[1]), .areset(in_areset), .bump_left(in_bump_left), .bump_right(in_bump_right), .ground(in_ground), .dig(in_dig), .walk_left(candidate_walk_left), .walk_right(candidate_walk_right), .aaah(candidate_aaah), .digging(candidate_digging));
assign candidate = {candidate_walk_left, candidate_walk_right, candidate_aaah, candidate_digging};
endmodule
