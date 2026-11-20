module top_module(
	input clk,
	input [7:0] d,
	input reset,
	output reg [7:0] q);
	
	always @(posedge clk)
		if (reset)
			q[7:0] <= {8{1'b1}}; // Change: Set q to all 1s on reset
		else
			q <= d;
	
endmodule
