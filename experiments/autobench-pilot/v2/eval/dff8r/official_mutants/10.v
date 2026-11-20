module top_module(
	input clk,
	input [7:0] d,
	input reset,
	output reg [7:0] q);
	
	always @(posedge clk)
		if (reset)
			q <= 0;
		else
			q <= {1'b1, d[7:1]}; // Change: Most significant bit of d set to 1 before assignment
	
endmodule
