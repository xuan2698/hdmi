module audit(input wire [0:0] in_rst, input wire [3:0] in_data_in, input wire [0:0] in_has_data_to_send, output wire [11:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_rst;
reg [3:0] previous_data_in;
reg [0:0] previous_has_data_to_send;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_rst <= in_rst;
previous_data_in <= in_data_in;
previous_has_data_to_send <= in_has_data_to_send;
end
assign permit = (first || phase[0] || ((in_rst == previous_rst) && (in_data_in == previous_data_in) && (in_has_data_to_send == previous_has_data_to_send))) && (!startup || ((in_rst == 1)));
wire [3:0] gold_data_out;
wire [3:0] gold_token_received;
wire [3:0] gold_token;
wire [3:0] candidate_data_out;
wire [3:0] candidate_token_received;
wire [3:0] candidate_token;
cvdp_r_token_ring_fsm gold_dut (.clk(phase[1]), .rst(in_rst), .data_in(in_data_in), .has_data_to_send(in_has_data_to_send), .data_out(gold_data_out), .token_received(gold_token_received), .token(gold_token));
assign gold = {gold_data_out, gold_token_received, gold_token};
cvdp_m_token_ring_fsm candidate_dut (.clk(phase[1]), .rst(in_rst), .data_in(in_data_in), .has_data_to_send(in_has_data_to_send), .data_out(candidate_data_out), .token_received(candidate_token_received), .token(candidate_token));
assign candidate = {candidate_data_out, candidate_token_received, candidate_token};
endmodule
