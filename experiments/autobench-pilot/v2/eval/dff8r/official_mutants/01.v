module top_module(
	input clk,
	input [7:0] d,
	input reset,
	output reg [7:0] q);
	
	always @(posedge clk)
		if (reset)
			q <= 8'hFF; // Change: q reset value changed from 0 to 0xFF
		else
			q <= d;
	
endmodule
