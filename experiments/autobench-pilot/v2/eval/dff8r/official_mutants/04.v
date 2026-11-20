module top_module(
	input clk,
	input [7:0] d,
	input reset,
	output reg [7:0] q);
	
	always @(posedge clk)
		if (reset)
			q <= 0;
		else
			q <= {d[6:0], 1'b0}; // Change: Least significant bit of d set to 0 before assignment
	
endmodule
