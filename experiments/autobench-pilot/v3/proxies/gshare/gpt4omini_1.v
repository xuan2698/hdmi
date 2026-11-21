module top_module(
    input clk,
    input areset, 

    input predict_valid,
    input [6:0] predict_pc,
    output reg predict_taken, 
    output reg [6:0] predict_history,

    input train_valid,
    input train_taken,
    input train_mispredicted,
    input [6:0] train_history, 
    input [6:0] train_pc
);

    reg [1:0] PHT[127:0]; // Pattern History Table with 128 entries of 2-bit saturating counters
    reg [6:0] global_history; // 7-bit global history register

    wire [6:0] predict_index = predict_pc ^ global_history; // Hashing the PC and global history
    wire [6:0] train_index = train_pc ^ train_history; // Hashing for training

    always @(posedge clk or posedge areset) begin
        if (areset) begin
            global_history <= 7'b0;
            for (int i = 0; i < 128; i++) begin
                PHT[i] <= 2'b00; // Initialize PHT to 0 (strongly not taken)
            end
        end else begin
            if (train_valid) begin
                if (train_mispredicted) begin
                    // Recover history for misprediction
                    global_history <= train_history;
                end else begin
                    // Update history on correct prediction
                    global_history <= {global_history[5:0], train_taken};
                end
                
                // Update PHT based on training outcome
                case (PHT[train_index])
                    2'b00: PHT[train_index] <= train_taken ? 2'b01 : 2'b00;
                    2'b01: PHT[train_index] <= train_taken ? 2'b10 : 2'b00;
                    2'b10: PHT[train_index] <= train_taken ? 2'b11 : 2'b01;
                    2'b11: PHT[train_index] <= train_taken ? 2'b11 : 2'b10;
                endcase
            end
            
            // Predict
            if (predict_valid) begin
                predict_taken <= (PHT[predict_index] == 2'b10 || PHT[predict_index] == 2'b11);
                predict_history <= global_history;
            end
        end
    end
endmodule
