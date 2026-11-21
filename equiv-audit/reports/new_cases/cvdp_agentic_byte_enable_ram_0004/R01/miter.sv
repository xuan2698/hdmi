module audit(input wire [12:0] in_addr_a, input wire [0:0] in_en_a, input wire [3:0] in_be_a, input wire [31:0] in_data_in_a, input wire [12:0] in_addr_b, input wire [0:0] in_en_b, input wire [3:0] in_be_b, input wire [31:0] in_data_in_b, output wire [63:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [12:0] previous_addr_a;
reg [0:0] previous_en_a;
reg [3:0] previous_be_a;
reg [31:0] previous_data_in_a;
reg [12:0] previous_addr_b;
reg [0:0] previous_en_b;
reg [3:0] previous_be_b;
reg [31:0] previous_data_in_b;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_addr_a <= in_addr_a;
previous_en_a <= in_en_a;
previous_be_a <= in_be_a;
previous_data_in_a <= in_data_in_a;
previous_addr_b <= in_addr_b;
previous_en_b <= in_en_b;
previous_be_b <= in_be_b;
previous_data_in_b <= in_data_in_b;
end
assign permit = (first || phase[0] || ((in_addr_a == previous_addr_a) && (in_en_a == previous_en_a) && (in_be_a == previous_be_a) && (in_data_in_a == previous_data_in_a) && (in_addr_b == previous_addr_b) && (in_en_b == previous_en_b) && (in_be_b == previous_be_b) && (in_data_in_b == previous_data_in_b))) && (!startup || (1'b1));
wire [31:0] gold_data_out_a;
wire [31:0] gold_data_out_b;
wire [31:0] candidate_data_out_a;
wire [31:0] candidate_data_out_b;
cvdp_r_custom_byte_enable_ram gold_dut (.clk(phase[1]), .addr_a(in_addr_a), .en_a(in_en_a), .be_a(in_be_a), .data_in_a(in_data_in_a), .addr_b(in_addr_b), .en_b(in_en_b), .be_b(in_be_b), .data_in_b(in_data_in_b), .data_out_a(gold_data_out_a), .data_out_b(gold_data_out_b));
assign gold = {gold_data_out_a, gold_data_out_b};
cvdp_m_custom_byte_enable_ram candidate_dut (.clk(phase[1]), .addr_a(in_addr_a), .en_a(in_en_a), .be_a(in_be_a), .data_in_a(in_data_in_a), .addr_b(in_addr_b), .en_b(in_en_b), .be_b(in_be_b), .data_in_b(in_data_in_b), .data_out_a(candidate_data_out_a), .data_out_b(candidate_data_out_b));
assign candidate = {candidate_data_out_a, candidate_data_out_b};
endmodule
