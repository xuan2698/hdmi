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
    wire [6:0] predict_index, train_index;
    
    assign predict_index = predict_pc ^ global_history;
    assign train_index = train_pc ^ train_history;
    
    assign predict_taken = pht[predict_index][1];
    assign predict_history = global_history;
    
    integer i;
    always @(posedge clk or posedge areset) begin
        if (areset) begin
            global_history <= 7'b0;
            for (i = 0; i < 128; i = i + 1)
                pht[i] <= 2'b01;
        end else begin
            if (train_valid && train_mispredicted)
                global_history <= {train_history[5:0], train_taken};
            else if (predict_valid)
                global_history <= {global_history[5:0], predict_taken};
                
            if (train_valid) begin
                case (pht[train_index])
                    2'b00: pht[train_index] <= train_taken ? 2'b01 : 2'b00;
                    2'b01: pht[train_index] <= train_taken ? 2'b10 : 2'b00;
                    2'b10: pht[train_index] <= train_taken ? 2'b11 : 2'b01;
                    2'b11: pht[train_index] <= train_taken ? 2'b11 : 2'b10;
                endcase
            end
        end
    end

endmodule