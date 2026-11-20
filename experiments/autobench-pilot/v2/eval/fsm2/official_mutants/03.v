module top_module (
	input clk,
	input j,
	input k,
	input areset,
	output out
);
	parameter A=0, B=1;
	reg state;
	reg next;
    
    always_comb begin
		case (state)
			A: next = j ? A : A; // Changed B to A for the true case
			B: next = k ? A : B;
		endcase
    end
    
    always @(posedge clk, posedge areset) begin
		if (areset) state <= B; // Changed initial state to B
        else state <= next;
	end
		
	assign out = (state==B);

endmodule
