module top_module(
	input clk,
	input [7:0] d,
	input reset,
	output reg [7:0] q);
	
	always @(negedge clk or negedge reset) // Added sensitivity to negedge of reset
		if (reset)
			q <= 8'h34;
		else
			q <= d;
	
endmodule
