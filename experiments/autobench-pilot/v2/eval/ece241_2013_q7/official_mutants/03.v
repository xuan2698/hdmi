module top_module (
	input clk,
	input j,
	input k,
	output reg Q
);

	always @(posedge clk)
		Q <= j|~k&Q; // Changed & to | between j and ~Q
endmodule
