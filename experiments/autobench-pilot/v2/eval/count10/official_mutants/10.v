module top_module(
	input clk,
	input reset,
	output reg [3:0] q = 4'b0001); // Initialized q with 1 instead of default 0

	always @(posedge clk)
		if (reset || q == 9)
			q <= 0;
		else
			q <= q+1;
	
endmodule
