module top_module (
	input clk,
	input a, 
	output reg [2:0] q
);

	always @(posedge clk)
		if (a)
			q <= 4; // No change
		else if (q == 5)  // Changed comparison value from 6 to 5
			q <= 0;
		else
			q <= q + 1'b1;

endmodule
