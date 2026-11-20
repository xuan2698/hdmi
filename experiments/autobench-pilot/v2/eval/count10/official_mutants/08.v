module top_module(
	input clk,
	input reset,
	output reg [3:0] q);
	
	always @(posedge clk)
		if (!reset && q == 9) // Changed reset condition to be active low
			q <= 0;
		else
			q <= q+1;
	
endmodule
