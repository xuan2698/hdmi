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
			q <= d & r; // Logical AND operation with reset signal, which will always be 0 when r is active
	end

endmodule
