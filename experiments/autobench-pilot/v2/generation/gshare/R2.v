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

    reg [1:0] PHT [127:0];  // 128-entry table of 2-bit saturating counters
    reg [6:0] global_history;

    // XOR-based hashing
    wire [6:0] predict_index = predict_pc ^ global_history;
    wire [6:0] train_index = train_pc ^ train_history;

    integer i;
    initial begin
        // Initialize the PHT and global history
        for (i = 0; i < 128; i = i + 1)
            PHT[i] = 2'b01; // Weakly not taken by default
        global_history = 7'b0;
    end

    // Prediction logic
    always @(*) begin
        if (predict_valid) begin
            predict_taken = PHT[predict_index] >= 2'b10;  // Predict taken if counter is 2 or 3
            predict_history = global_history;
        end
    end

    // Training and prediction update
    always @(posedge clk or posedge areset) begin
        if (areset) begin
            // Reset state
            for (i = 0; i < 128; i = i + 1)
                PHT[i] <= 2'b01; // Weakly not taken by default
            global_history <= 7'b0;
        end else begin
            if (train_valid) begin
                // Train the PHT using the true outcome
                if (train_taken) begin
                    // Increment the saturating counter
                    if (PHT[train_index] < 2'b11)
                        PHT[train_index] <= PHT[train_index] + 1;
                end else begin
                    // Decrement the saturating counter
                    if (PHT[train_index] > 2'b00)
                        PHT[train_index] <= PHT[train_index] - 1;
                end

                // Handle misprediction recovery
                if (train_mispredicted)
                    global_history <= {train_history[5:0], train_taken};
                else
                    global_history <= {global_history[5:0], predict_taken};
            end else if (predict_valid) begin
                // No training, update history with last prediction outcome
                global_history <= {global_history[5:0], predict_taken};
            end
        end
    end

endmodule
