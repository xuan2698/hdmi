module top_module(
	input clk,
	input [7:0] d,
	input reset,
	output reg [7:0] q);
	
	always @(negedge clk)
		if (reset)
			q <= d; // Changed to assign d instead of 0x34 on reset
		else
			q <= d;
	
endmodule
