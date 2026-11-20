module top_module(
	input clk,
	input L,
	input q_in,
	input r_in,
	output reg Q);

	initial Q=0;
	always @(negedge clk) // Changed to negedge of clk
		Q <= L ? r_in : q_in;
	
endmodule
