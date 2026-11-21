module audit(input wire [0:0] in_i_rst_b, input wire [15:0] in_i_data_in, input wire [0:0] in_i_enable, input wire [0:0] in_i_fault, input wire [0:0] in_i_clear, output wire [10:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_i_rst_b;
reg [15:0] previous_i_data_in;
reg [0:0] previous_i_enable;
reg [0:0] previous_i_fault;
reg [0:0] previous_i_clear;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_i_rst_b <= in_i_rst_b;
previous_i_data_in <= in_i_data_in;
previous_i_enable <= in_i_enable;
previous_i_fault <= in_i_fault;
previous_i_clear <= in_i_clear;
end
assign permit = (first || phase[0] || ((in_i_rst_b == previous_i_rst_b) && (in_i_data_in == previous_i_data_in) && (in_i_enable == previous_i_enable) && (in_i_fault == previous_i_fault) && (in_i_clear == previous_i_clear))) && (!startup || ((in_i_rst_b == 0)));
wire [0:0] gold_o_spi_cs_b;
wire [0:0] gold_o_spi_clk;
wire [0:0] gold_o_spi_data;
wire [4:0] gold_o_bits_left;
wire [0:0] gold_o_done;
wire [1:0] gold_o_fsm_state;
wire [0:0] candidate_o_spi_cs_b;
wire [0:0] candidate_o_spi_clk;
wire [0:0] candidate_o_spi_data;
wire [4:0] candidate_o_bits_left;
wire [0:0] candidate_o_done;
wire [1:0] candidate_o_fsm_state;
cvdp_r_spi_fsm gold_dut (.i_clk(phase[1]), .i_rst_b(in_i_rst_b), .i_data_in(in_i_data_in), .i_enable(in_i_enable), .i_fault(in_i_fault), .i_clear(in_i_clear), .o_spi_cs_b(gold_o_spi_cs_b), .o_spi_clk(gold_o_spi_clk), .o_spi_data(gold_o_spi_data), .o_bits_left(gold_o_bits_left), .o_done(gold_o_done), .o_fsm_state(gold_o_fsm_state));
assign gold = {gold_o_spi_cs_b, gold_o_spi_clk, gold_o_spi_data, gold_o_bits_left, gold_o_done, gold_o_fsm_state};
cvdp_m_spi_fsm candidate_dut (.i_clk(phase[1]), .i_rst_b(in_i_rst_b), .i_data_in(in_i_data_in), .i_enable(in_i_enable), .i_fault(in_i_fault), .i_clear(in_i_clear), .o_spi_cs_b(candidate_o_spi_cs_b), .o_spi_clk(candidate_o_spi_clk), .o_spi_data(candidate_o_spi_data), .o_bits_left(candidate_o_bits_left), .o_done(candidate_o_done), .o_fsm_state(candidate_o_fsm_state));
assign candidate = {candidate_o_spi_cs_b, candidate_o_spi_clk, candidate_o_spi_data, candidate_o_bits_left, candidate_o_done, candidate_o_fsm_state};
endmodule
