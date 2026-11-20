module top_module(
	input clk,
	input reset,
	output reg [3:0] q);
	
	always @(posedge clk)
		if (reset || q == 8) // Changed condition from q == 9 to q == 8
			q <= 0;
		else
			q <= q+1;
	
endmodule
