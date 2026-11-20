module top_module(
	input clk,
	input reset,
	output reg [3:0] q);
	
	always @(negedge clk) // Changed clock edge from posedge to negedge
		if (reset || q == 9)
			q <= 0;
		else
			q <= q+1;
	
endmodule
