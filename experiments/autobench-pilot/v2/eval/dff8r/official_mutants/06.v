module top_module(
	input clk,
	input [7:0] d,
	input reset,
	output reg [7:0] q);
	
	always @(posedge clk)
		q <= reset ? 8'b10101010 : d; // Change: q reset value changed to a pattern 0xAA
	
endmodule
