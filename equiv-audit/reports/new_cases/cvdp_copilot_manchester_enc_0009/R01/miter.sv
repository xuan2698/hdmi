module audit(input wire [0:0] in_rst_in, input wire [0:0] in_enc_valid_in, input wire [7:0] in_enc_data_in, input wire [0:0] in_dec_valid_in, input wire [15:0] in_dec_data_in, output wire [25:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_rst_in;
reg [0:0] previous_enc_valid_in;
reg [7:0] previous_enc_data_in;
reg [0:0] previous_dec_valid_in;
reg [15:0] previous_dec_data_in;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_rst_in <= in_rst_in;
previous_enc_valid_in <= in_enc_valid_in;
previous_enc_data_in <= in_enc_data_in;
previous_dec_valid_in <= in_dec_valid_in;
previous_dec_data_in <= in_dec_data_in;
end
assign permit = (first || phase[0] || ((in_rst_in == previous_rst_in) && (in_enc_valid_in == previous_enc_valid_in) && (in_enc_data_in == previous_enc_data_in) && (in_dec_valid_in == previous_dec_valid_in) && (in_dec_data_in == previous_dec_data_in))) && (!startup || ((in_rst_in == 1)));
wire [0:0] gold_enc_valid_out;
wire [15:0] gold_enc_data_out;
wire [0:0] gold_dec_valid_out;
wire [7:0] gold_dec_data_out;
wire [0:0] candidate_enc_valid_out;
wire [15:0] candidate_enc_data_out;
wire [0:0] candidate_dec_valid_out;
wire [7:0] candidate_dec_data_out;
cvdp_r_top_manchester gold_dut (.clk_in(phase[1]), .rst_in(in_rst_in), .enc_valid_in(in_enc_valid_in), .enc_data_in(in_enc_data_in), .dec_valid_in(in_dec_valid_in), .dec_data_in(in_dec_data_in), .enc_valid_out(gold_enc_valid_out), .enc_data_out(gold_enc_data_out), .dec_valid_out(gold_dec_valid_out), .dec_data_out(gold_dec_data_out));
assign gold = {gold_enc_valid_out, gold_enc_data_out, gold_dec_valid_out, gold_dec_data_out};
cvdp_m_top_manchester candidate_dut (.clk_in(phase[1]), .rst_in(in_rst_in), .enc_valid_in(in_enc_valid_in), .enc_data_in(in_enc_data_in), .dec_valid_in(in_dec_valid_in), .dec_data_in(in_dec_data_in), .enc_valid_out(candidate_enc_valid_out), .enc_data_out(candidate_enc_data_out), .dec_valid_out(candidate_dec_valid_out), .dec_data_out(candidate_dec_data_out));
assign candidate = {candidate_enc_valid_out, candidate_enc_data_out, candidate_dec_valid_out, candidate_dec_data_out};
endmodule
