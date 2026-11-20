module top_module(
	input clk,
	input [7:0] d,
	input reset,
	output reg [7:0] q);
	
	always @(posedge clk)
		if (reset)
			q <= 0;
		else
			q <= d << 1; // Change: Left shift d by 1 before assignment
	
endmodule
