module formal_top(input [0:0] in_areset, input [0:0] in_predict_valid, input [0:0] in_predict_taken, input [0:0] in_train_mispredicted, input [0:0] in_train_taken, input [31:0] in_train_history);
wire [31:0] gold, candidate, gold_x, candidate_x;
wire [1:0] phase, phase_x;
wire permit, permit_x;
audit core (.in_areset(in_areset), .in_predict_valid(in_predict_valid), .in_predict_taken(in_predict_taken), .in_train_mispredicted(in_train_mispredicted), .in_train_taken(in_train_taken), .in_train_history(in_train_history), .gold_d(gold), .candidate_d(candidate), .gold_x(gold_x),
    .candidate_x(candidate_x), .phase_d(phase), .phase_x(phase_x), .permit_d(permit), .permit_x(permit_x));
always @* begin
    assume (permit && !permit_x);
    assert ((((gold ^ candidate) | candidate_x) & ~gold_x) == 0);
end
endmodule
