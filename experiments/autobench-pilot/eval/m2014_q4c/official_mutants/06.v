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
			q <= d;
	end
	assign q = r ? 0 : q; // Added a continuous assignment conflicting with the always block
endmodule
