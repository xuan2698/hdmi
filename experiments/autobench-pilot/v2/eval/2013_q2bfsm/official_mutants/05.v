module top_module (
	input clk,
	input resetn,
	input x,
	input y,
	output f,
	output g
);
	parameter A=0, B=1, S0=2, S1=3, S10=4, G1=5, G2=6, P0=7, P1=8; // unchanged
	reg [3:0] state, next;

	always @(posedge clk) begin
		if (~resetn) state <= A; // unchanged
		else state <= next; // unchanged
	end
	
	always_comb begin
		case (state)
			A: next = B; // unchanged
			B: next = S0; // unchanged
			S0: next = x ? S1 : S0; // unchanged
			S1: next = x ? S1 : S10; // unchanged
			S10: next = x ? S0 : G1; // changed G1 to S0 in S10 state transition
			G1: next = y ? P1 : G2; // unchanged
			G2: next = y ? P1 : P0; // unchanged
			P0: next = P0; // unchanged
			P1: next = P1; // unchanged
			default: next = 'x; // unchanged
		endcase
	end
	
	assign f = (state == B); // unchanged
	assign g = (state == G1) || (state == G2) || (state == P1); // unchanged
endmodule
