module top_module (
	input clk,
	input a,
	input b,
	output reg q,
	output reg state
);

always @(posedge clk) begin
    if (a && b)
        state <= 1;
    else
        state <= 0;
        
    if (a && b)
        q <= ~q;
    else
        q <= state;
end

endmodule
