module top_module (
	input clk,
	input j,
	input k,
	output reg Q
);

	always @(posedge clk)
		Q <= j&~Q | ~k&Q | j&k; // Added j&k condition
endmodule
