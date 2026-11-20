module top_module (
	input clk,
	input j,
	input k,
	output reg Q
);

	always @(posedge clk)
		Q <= j | ~k&Q; // Removed the &~Q in j&~Q
endmodule
