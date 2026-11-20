module top_module(
	input clk,
	input reset,
	output reg [3:0] q);
	
	always @(posedge clk)
		if (reset || q == 11) // Changed comparison from q == 10 to q == 11
			q <= 1;
		else
			q <= q+1;
	
endmodule
