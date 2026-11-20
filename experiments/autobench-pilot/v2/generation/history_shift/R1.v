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

    logic [31:0] current_history;

    always_ff @(posedge clk or posedge areset) begin
        if (areset) begin
            current_history <= 32'b0;
        end else if (train_mispredicted) begin
            current_history <= {train_history[30:0], train_taken};
        end else if (predict_valid) begin
            current_history <= {current_history[30:0], predict_taken};
        end
    end

    assign predict_history = current_history;

endmodule
