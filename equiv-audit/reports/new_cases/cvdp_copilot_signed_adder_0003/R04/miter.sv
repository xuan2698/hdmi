module audit(input wire [0:0] in_i_rst_n, input wire [0:0] in_i_start, input wire [0:0] in_i_enable, input wire [0:0] in_i_mode, input wire [0:0] in_i_clear, input wire [7:0] in_i_operand_a, input wire [7:0] in_i_operand_b, output wire [11:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_i_rst_n;
reg [0:0] previous_i_start;
reg [0:0] previous_i_enable;
reg [0:0] previous_i_mode;
reg [0:0] previous_i_clear;
reg [7:0] previous_i_operand_a;
reg [7:0] previous_i_operand_b;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_i_rst_n <= in_i_rst_n;
previous_i_start <= in_i_start;
previous_i_enable <= in_i_enable;
previous_i_mode <= in_i_mode;
previous_i_clear <= in_i_clear;
previous_i_operand_a <= in_i_operand_a;
previous_i_operand_b <= in_i_operand_b;
end
assign permit = (first || phase[0] || ((in_i_rst_n == previous_i_rst_n) && (in_i_start == previous_i_start) && (in_i_enable == previous_i_enable) && (in_i_mode == previous_i_mode) && (in_i_clear == previous_i_clear) && (in_i_operand_a == previous_i_operand_a) && (in_i_operand_b == previous_i_operand_b))) && (!startup || ((in_i_rst_n == 0)));
wire [7:0] gold_o_resultant_sum;
wire [0:0] gold_o_overflow;
wire [0:0] gold_o_ready;
wire [1:0] gold_o_status;
wire [7:0] candidate_o_resultant_sum;
wire [0:0] candidate_o_overflow;
wire [0:0] candidate_o_ready;
wire [1:0] candidate_o_status;
cvdp_r_signedadder gold_dut (.i_clk(phase[1]), .i_rst_n(in_i_rst_n), .i_start(in_i_start), .i_enable(in_i_enable), .i_mode(in_i_mode), .i_clear(in_i_clear), .i_operand_a(in_i_operand_a), .i_operand_b(in_i_operand_b), .o_resultant_sum(gold_o_resultant_sum), .o_overflow(gold_o_overflow), .o_ready(gold_o_ready), .o_status(gold_o_status));
assign gold = {gold_o_resultant_sum, gold_o_overflow, gold_o_ready, gold_o_status};
cvdp_m_signedadder candidate_dut (.i_clk(phase[1]), .i_rst_n(in_i_rst_n), .i_start(in_i_start), .i_enable(in_i_enable), .i_mode(in_i_mode), .i_clear(in_i_clear), .i_operand_a(in_i_operand_a), .i_operand_b(in_i_operand_b), .o_resultant_sum(candidate_o_resultant_sum), .o_overflow(candidate_o_overflow), .o_ready(candidate_o_ready), .o_status(candidate_o_status));
assign candidate = {candidate_o_resultant_sum, candidate_o_overflow, candidate_o_ready, candidate_o_status};
endmodule
