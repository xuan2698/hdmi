module top_module (
	input clk,
	input d,
	input r,
	output logic q
);

	always@(posedge clk) begin
		if (r)
			q <= 0;
		else
			q <= d | r; // Logical OR with reset, effectively unchanged behavior but introduces redundancy
	end

endmodule
