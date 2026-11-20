module top_module(
	input clk,
	input [7:0] d,
	input reset,
	output reg [7:0] q);
	
	always @(negedge clk)
		if (reset)
			q <= 8'hFF; // Changed reset value to 0xFF
		else
			q <= d;
	
endmodule
