module top_module(
	input clk,
	input reset,
	input [31:0] in,
	output reg [31:0] out);
	
	reg [31:0] d_last;	
	
	always @(posedge clk) begin
		d_last <= in;
		if (reset)
			out <= {out[30:0], out[31]}; // Change: Bit rotation in out assignment on reset
		else
			out <= out | (~in & d_last);
	end
	
endmodule
