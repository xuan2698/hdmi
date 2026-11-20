module top_module(
	input clk,
	input [7:0] d,
	input reset,
	output reg [7:0] q);
	
	always @(posedge clk)
		if (reset)
			q <= 0;
		else
			q <= d ^ 8'hFF; // Change: XOR operation with all 1's to flip bits of d before assignment
	
endmodule
