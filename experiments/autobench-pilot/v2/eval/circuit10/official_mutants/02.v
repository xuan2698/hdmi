module top_module (
	input clk,
	input a,
	input b,
	output q,
	output state
);

	reg c;
	always @(posedge clk)
		c <= a&b | a&c; // Removed | b&c from the original logic.

	assign q = a^b^c;
	assign state = c;
			
endmodule
