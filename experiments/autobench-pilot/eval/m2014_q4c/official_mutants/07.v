module top_module (
	input clk,
	input d,
	input r,
	output logic q
);

	always@(posedge clk or posedge r) begin // Added posedge r to the sensitivity list
		if (r)
			q <= 0;
		else
			q <= d;
	end

endmodule
