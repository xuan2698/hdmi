module top_module (
	input clk,
	input j,
	input k,
	output reg Q
);

	always @(posedge clk)
		Q <= j&~Q | ~k; // Removed the Q in ~k&Q
endmodule
