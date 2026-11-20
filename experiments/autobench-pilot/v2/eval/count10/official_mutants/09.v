module top_module(
	input clk,
	input reset,
	output reg [3:0] q);
	
	always @(posedge clk)
		if (reset) // Simplified condition to only check reset
			q <= 0;
		else if (q == 9) // Moved q == 9 check to an else if block
			q <= 0;
		else
			q <= q+1;
	
endmodule
