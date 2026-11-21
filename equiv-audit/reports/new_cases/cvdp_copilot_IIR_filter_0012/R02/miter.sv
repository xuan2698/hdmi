module audit(input wire [0:0] in_reset, input wire [15:0] in_in_1, input wire [15:0] in_in_2, input wire [15:0] in_in_3, input wire [1:0] in_filter_select, output wire [47:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_reset;
reg [15:0] previous_in_1;
reg [15:0] previous_in_2;
reg [15:0] previous_in_3;
reg [1:0] previous_filter_select;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_reset <= in_reset;
previous_in_1 <= in_in_1;
previous_in_2 <= in_in_2;
previous_in_3 <= in_in_3;
previous_filter_select <= in_filter_select;
end
assign permit = (first || phase[0] || ((in_reset == previous_reset) && (in_in_1 == previous_in_1) && (in_in_2 == previous_in_2) && (in_in_3 == previous_in_3) && (in_filter_select == previous_filter_select))) && (!startup || ((in_reset == 1)));
wire [15:0] gold_out_1;
wire [15:0] gold_out_2;
wire [15:0] gold_out_3;
wire [15:0] candidate_out_1;
wire [15:0] candidate_out_2;
wire [15:0] candidate_out_3;
cvdp_r_iir_filt gold_dut (.clk(phase[1]), .reset(in_reset), .in_1(in_in_1), .in_2(in_in_2), .in_3(in_in_3), .filter_select(in_filter_select), .out_1(gold_out_1), .out_2(gold_out_2), .out_3(gold_out_3));
assign gold = {gold_out_1, gold_out_2, gold_out_3};
cvdp_m_iir_filt candidate_dut (.clk(phase[1]), .reset(in_reset), .in_1(in_in_1), .in_2(in_in_2), .in_3(in_in_3), .filter_select(in_filter_select), .out_1(candidate_out_1), .out_2(candidate_out_2), .out_3(candidate_out_3));
assign candidate = {candidate_out_1, candidate_out_2, candidate_out_3};
endmodule
