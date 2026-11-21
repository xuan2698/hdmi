module audit(input wire [0:0] in_reset, input wire [0:0] in_start, input wire [14:0] in_plaintext, input wire [44:0] in_key, output wire [15:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_reset;
reg [0:0] previous_start;
reg [14:0] previous_plaintext;
reg [44:0] previous_key;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_reset <= in_reset;
previous_start <= in_start;
previous_plaintext <= in_plaintext;
previous_key <= in_key;
end
assign permit = (first || phase[0] || ((in_reset == previous_reset) && (in_start == previous_start) && (in_plaintext == previous_plaintext) && (in_key == previous_key))) && (!startup || ((in_reset == 1)));
wire [14:0] gold_ciphertext;
wire [0:0] gold_done;
wire [14:0] candidate_ciphertext;
wire [0:0] candidate_done;
cvdp_r_hill_cipher gold_dut (.clk(phase[1]), .reset(in_reset), .start(in_start), .plaintext(in_plaintext), .key(in_key), .ciphertext(gold_ciphertext), .done(gold_done));
assign gold = {gold_ciphertext, gold_done};
cvdp_m_hill_cipher candidate_dut (.clk(phase[1]), .reset(in_reset), .start(in_start), .plaintext(in_plaintext), .key(in_key), .ciphertext(candidate_ciphertext), .done(candidate_done));
assign candidate = {candidate_ciphertext, candidate_done};
endmodule
