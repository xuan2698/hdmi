module top_module(
	input clk,
	input reset,
	output reg [2:0] q); // Changed bit width from [3:0] to [2:0]
	
	always @(posedge clk)
		if (reset || q == 10)
			q <= 1;
		else
			q <= q+1;
	
endmodule
