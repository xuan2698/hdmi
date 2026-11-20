module top_module(
	input clk,
	input [7:0] d,
	input reset,
	output reg [7:0] q);
	
	always @(posedge clk or posedge reset) // Change: Added reset as a trigger in always block
		if (reset)
			q <= 0;
		else
			q <= d;
	
endmodule
