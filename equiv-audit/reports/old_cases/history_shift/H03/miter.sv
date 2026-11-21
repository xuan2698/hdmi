module audit(input wire [0:0] in_areset, input wire [0:0] in_predict_valid, input wire [0:0] in_predict_taken, input wire [0:0] in_train_mispredicted, input wire [0:0] in_train_taken, input wire [31:0] in_train_history, output wire [31:0] gold, candidate, output wire [1:0] phase, output wire permit);
reg [1:0] phase_counter = 0;
assign phase = phase_counter;
reg first = 1;
reg startup = 1;
reg [0:0] previous_areset;
reg [0:0] previous_predict_valid;
reg [0:0] previous_predict_taken;
reg [0:0] previous_train_mispredicted;
reg [0:0] previous_train_taken;
reg [31:0] previous_train_history;
always @($global_clock) begin
  phase_counter <= phase_counter + 1'b1;
  first <= 0;
  if (&phase_counter) startup <= 0;
  previous_areset <= in_areset;
previous_predict_valid <= in_predict_valid;
previous_predict_taken <= in_predict_taken;
previous_train_mispredicted <= in_train_mispredicted;
previous_train_taken <= in_train_taken;
previous_train_history <= in_train_history;
end
assign permit = (first || phase[0] || ((in_areset == previous_areset) && (in_predict_valid == previous_predict_valid) && (in_predict_taken == previous_predict_taken) && (in_train_mispredicted == previous_train_mispredicted) && (in_train_taken == previous_train_taken) && (in_train_history == previous_train_history))) && (!startup || ((in_areset == 1)));
wire [31:0] gold_predict_history;
wire [31:0] candidate_predict_history;
cvdp_r_top_module gold_dut (.clk(phase[1]), .areset(in_areset), .predict_valid(in_predict_valid), .predict_taken(in_predict_taken), .train_mispredicted(in_train_mispredicted), .train_taken(in_train_taken), .train_history(in_train_history), .predict_history(gold_predict_history));
assign gold = {gold_predict_history};
cvdp_m_top_module candidate_dut (.clk(phase[1]), .areset(in_areset), .predict_valid(in_predict_valid), .predict_taken(in_predict_taken), .train_mispredicted(in_train_mispredicted), .train_taken(in_train_taken), .train_history(in_train_history), .predict_history(candidate_predict_history));
assign candidate = {candidate_predict_history};
endmodule
