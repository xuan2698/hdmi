module top_module (
	input clk,
	input j,
	input k,
	output reg Q
);

	always @(posedge clk)
		Q <= j&~Q | ~k&Q ^ j; // Added XOR with j at the end
endmodule
