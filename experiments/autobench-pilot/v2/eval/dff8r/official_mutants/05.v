module top_module(
	input clk,
	input [7:0] d,
	input reset,
	output reg [7:0] q);
	
	always @(negedge clk) // Change: Triggered on the negative edge of clk instead of positive
		if (reset)
			q <= 0;
		else
			q <= d;
	
endmodule
