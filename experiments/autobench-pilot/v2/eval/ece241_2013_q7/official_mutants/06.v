module top_module (
	input clk,
	input j,
	input k,
	output reg Q
);

	always @(posedge clk)
		Q <= j&~Q; // Removed the ~k&Q part
endmodule
