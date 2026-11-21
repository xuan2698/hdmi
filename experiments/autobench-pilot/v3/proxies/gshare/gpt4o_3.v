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

	reg [6:0] global_history;
	reg [1:0] pht [0:127]; // 128-entry table of 2-bit saturating counters
	integer i;

	always @(posedge clk or posedge areset) begin
		if (areset) begin
			global_history <= 7'b0;
			for (i = 0; i < 128; i = i + 1) begin
				pht[i] <= 2'b01; // Weakly not-taken (initializing the PHT)
			end
		end else begin
			if (train_valid) begin
				// Calculate the index for training
				integer train_index = train_pc ^ train_history;
				// Update PHT
				if (train_taken) begin
					// Increment saturating counter if taken
					if (pht[train_index] != 2'b11) begin
						pht[train_index] <= pht[train_index] + 1;
					end
				end else begin
					// Decrement saturating counter if not taken
					if (pht[train_index] != 2'b00) begin
						pht[train_index] <= pht[train_index] - 1;
					end
				end
				// Update global history after misprediction recovery
				if (train_mispredicted) begin
					global_history <= {train_history[5:0], train_taken};
				end
			end
			// Update global history with predicted outcome
			if (!train_valid && predict_valid) begin
				global_history <= {global_history[5:0], predict_taken};
			end
		end
	end

	always @(*) begin
		// Default values
		predict_taken = 1'b0;
		predict_history = global_history;

		if (predict_valid) begin
			// Calculate the index for prediction
			integer predict_index = predict_pc ^ global_history;
			// Access PHT to get prediction
			predict_taken = pht[predict_index][1];
			predict_history = global_history;
		end
	end

endmodule
