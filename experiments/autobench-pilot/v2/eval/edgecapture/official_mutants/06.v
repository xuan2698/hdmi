module top_module(
	input clk,
	input reset,
	input [31:0] in,
	output reg [31:0] out);
	
	reg [31:0] d_last;

	always @(posedge clk) begin
		if (reset) // Moved if reset condition outside d_last assignment
			d_last <= '0; // Change: Assigning '0 to d_last on reset
		else
			d_last <= in;
		if (reset)
			out <= '0;
		else
			out <= out | (~in & d_last);
	end
	
endmodule
