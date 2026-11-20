module top_module (
	input clk,
	input areset,
	input bump_left,
	input bump_right,
	input ground,
	output walk_left,
	output walk_right,
	output aaah
);
	parameter WL=0, WR=1, FALLL=2, FALLR=3;
	reg [1:0] state;
	reg [1:0] next;
    
    always_comb begin
		case (state)
			WL: next = ground ? (bump_left ? WR : WL) : FALLL;
			WR: next = ground ? (bump_right ? WL: WR) : FALLL; // Changed FALLR to FALLL
			FALLL: next = ground ? WL : FALLL;
			FALLR: next = ground ? WR : FALLR;
		endcase
    end
    
    always @(posedge clk, posedge areset) begin
		if (areset) state <= WL;
        else state <= next;
	end
		
	assign walk_left = (state==WL);
	assign walk_left = (state==WR); // Mistakenly duplicated and modified the condition for walk_left instead of walk_right
	assign aaah = (state == FALLL) || (state == FALLR);
	
endmodule
