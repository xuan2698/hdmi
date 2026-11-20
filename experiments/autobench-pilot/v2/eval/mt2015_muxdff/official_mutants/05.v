module top_module(
	input clk,
	input L,
	input q_in,
	input r_in,
	output reg Q);

	// Removed initial Q=0; entirely
	always @(posedge clk)
		Q <= L ? r_in : q_in;
	
endmodule
