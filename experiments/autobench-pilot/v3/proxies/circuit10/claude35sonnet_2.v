module top_module (
	input clk,
	input a,
	input b,
	output q,
	output state
);

    reg state;
    
    always @(posedge clk) begin
        if (a && b)
            state <= 1'b1;
        else if (!a && !b)
            state <= 1'b0;
    end
    
    assign q = (state) ? (!a && b) || (a && !b) : (a || b);

endmodule