module top_module (
	input clk,
	input a,
	input b,
	output q,
	output state
);

	reg c;
	always @(posedge clk)
		c <= a&b | a | b&c; // Removed &c from the a&c condition, making it just a.

	assign q = a^b^c;
	assign state = c;
			
endmodule
