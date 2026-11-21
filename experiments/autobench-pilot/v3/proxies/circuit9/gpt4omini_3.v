module top_module (
	input clk,
	input a, 
	output reg [2:0] q
);

	always @(posedge clk) begin
		if (a) begin
			if (q == 3'b111) 
				q <= 3'b000;
			else 
				q <= q + 1;
		end
	end

	always @(negedge clk) begin
		if (!a) 
			q <= q;
	end

endmodule
