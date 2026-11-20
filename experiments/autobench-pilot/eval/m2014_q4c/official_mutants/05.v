module top_module (
	input clk,
	input d,
	input r,
	output logic q
);

	always@(posedge clk) begin
		if (r)
			q <= d; // Assign d instead of 0 when reset is active
		else
			q <= d;
	end

endmodule
