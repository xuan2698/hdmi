module top_module(
	input clk,
	input [7:0] d,
	input reset,
	output reg [7:0] q);
	
	always @(negedge clk)
		if (reset)
			q[7:0] <= {8{1'b1}}; // Changed reset value to all 1's
		else
			q <= d;
	
endmodule
