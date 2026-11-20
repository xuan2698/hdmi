module top_module(
	input clk,
	input reset,
	output reg [3:0] q);
	
	always @(posedge clk)
		if (reset || q == 10) // Changed condition to q == 10, which is out of 4-bit range
			q <= 0;
		else
			q <= q+1;
	
endmodule
