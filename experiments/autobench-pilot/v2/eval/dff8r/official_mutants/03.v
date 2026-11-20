module top_module(
	input clk,
	input [7:0] d,
	input reset,
	output reg [7:0] q);
	
	always @(posedge clk)
		if (!reset) // Change: Inverted the condition check for reset
			q <= d;
		else
			q <= 0;
	
endmodule
