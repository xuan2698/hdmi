module top_module (
	input clk,
	input d,
	input r,
	output logic q
);

	always@(posedge clk) begin
		q <= r ? 1 : d; // Changed inline if condition to set q to 1 on reset
	end

endmodule
