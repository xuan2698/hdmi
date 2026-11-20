module top_module(
	input clk,
	input reset,
	output reg [3:0] q);
	
	always @(posedge clk)
		if (reset || q == 10)
			q <= 2; // Changed reset value from 1 to 2
		else
			q <= q+1;
	
endmodule
