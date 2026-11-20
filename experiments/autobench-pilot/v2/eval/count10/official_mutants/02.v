module top_module(
	input clk,
	input reset,
	output reg [3:0] q);
	
	always @(posedge clk)
		if (reset || q == 9)
			q <= 1; // Changed reset value from 0 to 1
		else
			q <= q+1;
	
endmodule
