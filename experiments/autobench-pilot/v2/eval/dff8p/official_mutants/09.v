module top_module(
	input clk,
	input [7:0] d,
	input reset,
	output reg [7:0] q);
	
	always @(negedge clk)
		if (reset)
			q <= 8'h34;
		else
			q[6:0] <= d[6:0]; // Only assigns bits 6:0 from d, not bit 7
			q[7] <= d[0]; // Bit 7 is assigned from bit 0 of d
	
endmodule
