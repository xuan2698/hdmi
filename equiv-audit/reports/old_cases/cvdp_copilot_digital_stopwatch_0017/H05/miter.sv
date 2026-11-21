module audit(input wire [0:0] in_reset, input wire [0:0] in_start_stop, output wire [12:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_reset;
reg [0:0] previous_start_stop;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_reset <= in_reset;
previous_start_stop <= in_start_stop;
end
assign permit = (first || phase[0] || ((in_reset == previous_reset) && (in_start_stop == previous_start_stop))) && (!startup || ((in_reset == 1)));
wire [5:0] gold_seconds;
wire [5:0] gold_minutes;
wire [0:0] gold_hour;
wire [5:0] candidate_seconds;
wire [5:0] candidate_minutes;
wire [0:0] candidate_hour;
cvdp_r_dig_stopwatch gold_dut (.clk(phase[1]), .reset(in_reset), .start_stop(in_start_stop), .seconds(gold_seconds), .minutes(gold_minutes), .hour(gold_hour));
assign gold = {gold_seconds, gold_minutes, gold_hour};
cvdp_m_dig_stopwatch candidate_dut (.clk(phase[1]), .reset(in_reset), .start_stop(in_start_stop), .seconds(candidate_seconds), .minutes(candidate_minutes), .hour(candidate_hour));
assign candidate = {candidate_seconds, candidate_minutes, candidate_hour};
endmodule
