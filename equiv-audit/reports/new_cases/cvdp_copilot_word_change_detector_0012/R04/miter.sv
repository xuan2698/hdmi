module audit(input wire [0:0] in_reset, input wire [7:0] in_data_in, input wire [7:0] in_mask, input wire [7:0] in_match_pattern, input wire [0:0] in_enable, input wire [0:0] in_latch_pattern, output wire [9:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_reset;
reg [7:0] previous_data_in;
reg [7:0] previous_mask;
reg [7:0] previous_match_pattern;
reg [0:0] previous_enable;
reg [0:0] previous_latch_pattern;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_reset <= in_reset;
previous_data_in <= in_data_in;
previous_mask <= in_mask;
previous_match_pattern <= in_match_pattern;
previous_enable <= in_enable;
previous_latch_pattern <= in_latch_pattern;
end
assign permit = (first || phase[0] || ((in_reset == previous_reset) && (in_data_in == previous_data_in) && (in_mask == previous_mask) && (in_match_pattern == previous_match_pattern) && (in_enable == previous_enable) && (in_latch_pattern == previous_latch_pattern))) && (!startup || ((in_reset == 1)));
wire [0:0] gold_word_change_pulse;
wire [0:0] gold_pattern_match_pulse;
wire [7:0] gold_latched_pattern;
wire [0:0] candidate_word_change_pulse;
wire [0:0] candidate_pattern_match_pulse;
wire [7:0] candidate_latched_pattern;
cvdp_r_Word_Change_Pulse gold_dut (.clk(phase[1]), .reset(in_reset), .data_in(in_data_in), .mask(in_mask), .match_pattern(in_match_pattern), .enable(in_enable), .latch_pattern(in_latch_pattern), .word_change_pulse(gold_word_change_pulse), .pattern_match_pulse(gold_pattern_match_pulse), .latched_pattern(gold_latched_pattern));
assign gold = {gold_word_change_pulse, gold_pattern_match_pulse, gold_latched_pattern};
cvdp_m_Word_Change_Pulse candidate_dut (.clk(phase[1]), .reset(in_reset), .data_in(in_data_in), .mask(in_mask), .match_pattern(in_match_pattern), .enable(in_enable), .latch_pattern(in_latch_pattern), .word_change_pulse(candidate_word_change_pulse), .pattern_match_pulse(candidate_pattern_match_pulse), .latched_pattern(candidate_latched_pattern));
assign candidate = {candidate_word_change_pulse, candidate_pattern_match_pulse, candidate_latched_pattern};
endmodule
