module top_module (
	input clk,
	input d,
	input r,
	output logic q
);

	always@(negedge clk) begin // Triggered on the negative edge of clk instead of positive
		if (r)
			q <= 0;
		else
			q <= d;
	end

endmodule
