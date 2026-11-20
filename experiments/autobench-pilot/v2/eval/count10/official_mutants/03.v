module top_module(
	input clk,
	input reset,
	output reg [3:0] q);
	
	always @(posedge clk)
		if (reset) // Removed the q == 9 condition
			q <= 0;
		else
			q <= q+1;
	
endmodule
