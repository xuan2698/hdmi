module top_module(
	input clk,
	input reset,
	input [31:0] in,
	output reg [31:0] out);
	
	reg [31:0] d_last;
	
	always @(posedge clk) begin
		d_last <= in;
		if (reset)
			out <= '1; // Change: '0 to '1 to create mutant
		else
			out <= out | (~in & d_last);
	end
	
endmodule
