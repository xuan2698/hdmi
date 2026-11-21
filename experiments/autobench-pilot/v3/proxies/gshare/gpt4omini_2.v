module top_module(
    input clk,
    input areset, 

    input predict_valid,
    input [6:0] predict_pc,
    output predict_taken, 
    output [6:0] predict_history,

    input train_valid,
    input train_taken,
    input train_mispredicted,
    input [6:0] train_history, 
    input [6:0] train_pc
);

    // Parameters
    parameter PHT_SIZE = 128;
    parameter BHT_SIZE = 7;

    // PHT and BHT
    reg [1:0] PHT [0:PHT_SIZE-1];
    reg [BHT_SIZE-1:0] BHT;

    // Index and next state logic
    wire [6:0] index;
    wire [6:0] hashed_pc;
    assign hashed_pc = predict_pc ^ BHT; // XOR based hasher
    assign index = hashed_pc[6:0];

    // Prediction
    assign predict_taken = (PHT[index] > 1); // Taken if state > 1
    
    always @(posedge clk or posedge areset) begin
        if (areset) begin
            // Reset PHT and BHT
            integer i;
            for (i = 0; i < PHT_SIZE; i = i + 1) begin
                PHT[i] <= 2'b00; // Initialize to 'Strongly Not Taken'
            end
            BHT <= 7'b0;
        end
        else begin
            // Training
            if (train_valid) begin
                if (train_mispredicted) begin
                    BHT <= train_history; // Recover history on misprediction
                end
                // Update PHT on training result
                if (train_taken) begin
                    if (PHT[train_pc] < 2'b11) PHT[train_pc] <= PHT[train_pc] + 1; // +1 to state
                end else begin
                    if (PHT[train_pc] > 2'b00) PHT[train_pc] <= PHT[train_pc] - 1; // -1 to state
                end
            end
            
            // Prediction update
            if (predict_valid) begin
                // Update BHT based on prediction
                BHT <= (BHT << 1) | predict_taken; // Shift and update BHT
            end
        end
    end

    // Output current state of BHT
    assign predict_history = BHT;

endmodule
