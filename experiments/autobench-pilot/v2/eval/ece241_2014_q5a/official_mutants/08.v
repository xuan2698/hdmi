module top_module (
	input clk,
	input areset,
	input x,
	output z
);

	parameter A=0,B=1,C=2;
	reg [1:0] state;
	always @(posedge clk, posedge areset) begin
		if (areset)
			state <= A;
		else begin
			case (state)
				A: state <= x ? C : A;
				B: state <= x ? C : B; // Changed C and B positions in this line
				C: state <= x ? B : C;
			endcase
		end
	end
	
	assign z = (state == B); // Changed condition to state == B
endmodule
