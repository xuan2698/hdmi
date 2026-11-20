module top_module (
	input clk,
	input areset,
	input x,
	output z
);

	parameter A=0,B=1,C=2,D=3; // Added a new state D
	reg [1:0] state;
	always @(posedge clk, posedge areset) begin
		if (areset)
			state <= A;
		else begin
			case (state)
				A: state <= x ? C : A;
				B: state <= x ? B : C;
				C: state <= x ? B : C;
				// D state is not used, just defined
			endcase
		end
	end
	
	assign z = (state == C);
	
endmodule
