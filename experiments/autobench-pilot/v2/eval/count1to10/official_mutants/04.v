module top_module(
	input clk,
	input reset,
	output reg [3:0] q);
	
	always @(posedge clk)
		if (reset)
			q <= 1; // Removed condition q == 10 for reset
		else
			q <= q+1;
	
endmodule
