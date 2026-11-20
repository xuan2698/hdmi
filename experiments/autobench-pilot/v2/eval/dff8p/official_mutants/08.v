module top_module(
	input clk,
	input [7:0] d,
	input reset,
	output reg [7:0] q);
	
	always @(negedge clk)
		if (reset)
			q <= 8'h34;
		else
			q[7:1] <= d[7:1]; // Only assigns bits 7:1 from d, not bit 0
			q[0] <= 1'b0; // Bit 0 is forced to 0
	
endmodule
