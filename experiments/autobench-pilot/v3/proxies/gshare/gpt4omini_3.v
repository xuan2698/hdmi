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

    reg [1:0] PHT [0:127]; // Pattern History Table
    reg [6:0] global_history; // Global Branch History Register

    wire [6:0] index;
    assign index = (predict_pc ^ global_history) % 128;

    always @(posedge clk or posedge areset) begin
        if (areset) begin
            global_history <= 7'b0;
            for (int i = 0; i < 128; i = i + 1) begin
                PHT[i] <= 2'b00; // Initialize PHT to "SNT"
            end
        end else begin
            // Prediction Logic
            if (predict_valid) begin
                predict_taken <= PHT[index][1]; // Taken if state is 2'b10 or 2'b11
                predict_history <= global_history;
            end
            
            // Training Logic
            if (train_valid) begin
                if (train_taken) begin
                    if (PHT[index] != 2'b11)
                        PHT[index] <= PHT[index] + 1; // Increment if not max
                end else begin
                    if (PHT[index] != 2'b00)
                        PHT[index] <= PHT[index] - 1; // Decrement if not min
                end
                
                // Update global history
                if (train_mispredicted) begin
                    global_history <= train_history; // Recover the global history
                end else begin
                    global_history <= {global_history[5:0], train_taken}; // Shift in new outcome
                end
            end
        end
    end
    
endmodule
