module top_module(
	input clk,
	input L,
	input q_in,
	input r_in,
	output reg Q);

	initial Q=0;
	always @(posedge clk)
		Q <= L ? r_in : {q_in}; // Enclosed q_in in braces, making it a single bit concatenation
	
endmodule
