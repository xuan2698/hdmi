module top_module
(
    input clk,
    input areset,
    input predict_valid,
    input predict_taken,
    output logic [31:0] predict_history,
    
    input train_mispredicted,
    input train_taken,
    input [31:0] train_history
);
    always@(posedge clk, posedge areset)
        if (areset) begin
            predict_history = 0;
        end else begin
            if (train_mispredicted)
                predict_history <= {train_taken, train_history}; // Swapped positions of train_taken and train_history
            else if (predict_valid)
                predict_history <= {predict_history, predict_taken};
        end
endmodule
