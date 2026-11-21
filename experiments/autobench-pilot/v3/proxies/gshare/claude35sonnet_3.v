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

    reg [1:0] pht [127:0];
    reg [6:0] global_history;
    
    wire [6:0] predict_index = predict_pc ^ global_history;
    wire [6:0] train_index = train_pc ^ train_history;
    
    assign predict_taken = pht[predict_index][1];
    assign predict_history = global_history;
    
    integer i;
    always @(posedge clk or posedge areset) begin
        if (areset) begin
            global_history <= 7'b0;
            for (i = 0; i < 128; i = i + 1) begin
                pht[i] <= 2'b01;
            end
        end else begin
            if (train_valid) begin
                if (train_taken && pht[train_index] != 2'b11)
                    pht[train_index] <= pht[train_index] + 1;
                else if (!train_taken && pht[train_index] != 2'b00)
                    pht[train_index] <= pht[train_index] - 1;
                
                if (train_mispredicted)
                    global_history <= {train_history[5:0], train_taken};
            end else if (predict_valid) begin
                global_history <= {global_history[5:0], predict_taken};
            end
        end
    end

endmodule