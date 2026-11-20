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
			A: next = j ? B : A;
			B: next = k ? B : A; // Changed A to B for the true case
		endcase
    end
    
    always @(posedge clk, posedge areset) begin
		if (areset) state <= A;
        else state <= next;
	end
		
	assign out = (state==A); // Changed state==B to state==A, which will always result in 0

endmodule
