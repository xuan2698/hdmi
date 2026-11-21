module top_module (
    input clk,
    input a,
    input b,
    output reg q,
    output reg state
);

    always @(posedge clk) begin
        if (a & b) begin
            q <= state;
            state <= ~state;
        end else if (a) begin
            state <= 1'b0;
            q <= state;
        end else if (b) begin
            state <= 1'b1;
            q <= state;
        end else begin
            q <= state;
        end
    end

endmodule
