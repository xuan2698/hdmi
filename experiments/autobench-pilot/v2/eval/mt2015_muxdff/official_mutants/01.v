module top_module(
	input clk,
	input L,
	input q_in,
	input r_in,
	output reg Q);

	initial Q=1; // Changed the initial value of Q to 1
	always @(posedge clk)
		Q <= L ? r_in : q_in;
	
endmodule
