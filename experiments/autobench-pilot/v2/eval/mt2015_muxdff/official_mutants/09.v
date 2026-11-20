module top_module(
	input clk,
	input L,
	input q_in,
	input r_in,
	output reg Q);

	initial Q=0;
	always @(posedge clk)
		Q <= L ? q_in : r_in; // Swapped the operands of the ternary operator
	
endmodule
