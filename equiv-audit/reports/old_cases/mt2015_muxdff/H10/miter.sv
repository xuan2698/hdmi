module audit(input wire [0:0] in_L, input wire [0:0] in_q_in, input wire [0:0] in_r_in, output wire [0:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_L;
reg [0:0] previous_q_in;
reg [0:0] previous_r_in;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_L <= in_L;
previous_q_in <= in_q_in;
previous_r_in <= in_r_in;
end
assign permit = (first || phase[0] || ((in_L == previous_L) && (in_q_in == previous_q_in) && (in_r_in == previous_r_in))) && (!startup || (1'b1));
wire [0:0] gold_Q;
wire [0:0] candidate_Q;
cvdp_r_top_module gold_dut (.clk(phase[1]), .L(in_L), .q_in(in_q_in), .r_in(in_r_in), .Q(gold_Q));
assign gold = {gold_Q};
cvdp_m_top_module candidate_dut (.clk(phase[1]), .L(in_L), .q_in(in_q_in), .r_in(in_r_in), .Q(candidate_Q));
assign candidate = {candidate_Q};
endmodule
