module top_module (
	input clk,
	input d,
	input r,
	output logic q
);

	always@(posedge clk) begin
		if (!r) // Changed the condition to negated reset
			q <= d;
		else
			q <= 0;
	end

endmodule
