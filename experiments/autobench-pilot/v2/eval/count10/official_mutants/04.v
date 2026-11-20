module top_module(
	input clk,
	input reset,
	output reg [3:0] q);
	
	always @(posedge clk)
		if (reset || q == 9)
			q <= 0;
		else
			q <= q + 2; // Changed increment from q+1 to q+2
	
endmodule
