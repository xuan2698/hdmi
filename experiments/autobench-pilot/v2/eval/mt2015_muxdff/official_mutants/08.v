module top_module(
	input clk,
	input L,
	input q_in,
	input r_in,
	output reg Q);

	initial Q=0;
	always @(posedge clk)
		Q <= L && q_in; // Changed the operation inside always block
	
endmodule
