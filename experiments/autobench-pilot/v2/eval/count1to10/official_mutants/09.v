module top_module(
	input clk,
	input reset,
	output reg [3:0] q);
	
	always @(posedge clk)
		if (!reset || q == 10) // Changed reset condition to !reset
			q <= 1;
		else
			q <= q+1;
	
endmodule
