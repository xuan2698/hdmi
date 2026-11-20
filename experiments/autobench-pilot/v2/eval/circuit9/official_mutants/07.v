module top_module (
	input clk,
	input a, 
	output reg [2:0] q
);

	always @(posedge clk)
		if (a)
			q <= 4;
		else if (q == 7) // Changed comparison value from 6 to 7, unreachable in 3 bits
			q <= 0;
		else
			q <= q + 1'b1;

endmodule
