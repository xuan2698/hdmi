module top_module (
	input clk,
	input areset,
	input x,
	output z
);

	parameter A=0,B=1,C=2;
	reg [2:0] state; // Changed state register size from [1:0] to [2:0]
	always @(posedge clk, posedge areset) begin
		if (areset)
			state <= A;
		else begin
			case (state)
				A: state <= x ? C : A;
				B: state <= x ? B : C;
				C: state <= x ? B : C;
			endcase
		end
	end
	
	assign z = (state == C);
	
endmodule
