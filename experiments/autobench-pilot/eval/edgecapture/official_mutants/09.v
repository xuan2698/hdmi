module top_module(
	input clk,
	input reset,
	input [31:0] in,
	output reg [31:0] out);
	
	reg [31:0] d_last;	
	
	always @(posedge clk) begin
		d_last <= {d_last[0], d_last[31:1]}; // Change: Bit shuffle for d_last
		if (reset)
			out <= '0;
		else
			out <= out | (~in & d_last);
	end
	
endmodule
