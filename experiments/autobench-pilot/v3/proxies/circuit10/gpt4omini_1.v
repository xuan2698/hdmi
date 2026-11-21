module top_module (
    input clk,
    input a,
    input b,
    output reg q,
    output reg state
);

    always @(posedge clk) begin
        state <= (state == 1 && b == 1) ? 0 : (state == 0 && a == 1) ? 1 : state;
        q <= (state == 1 && b == 1) ? 1 : (state == 0 && a == 1) ? 0 : q;
    end

    initial begin
        state = 0;
        q = 0;
    end

endmodule
