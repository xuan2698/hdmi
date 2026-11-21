module top_module (
    input clk,
    input a,
    input b,
    output reg q,
    output reg state
);

reg flip_flop;

always @(posedge clk) begin
    if (a && !b) begin
        flip_flop <= 1;
        q <= 1;
        state <= 1;
    end else if (!a && b) begin
        flip_flop <= 0;
        q <= 0;
        state <= 1;
    end else if (a && b) begin
        if (flip_flop) begin
            q <= 0;
            state <= 0;
        end else begin
            q <= 1;
            state <= 0;
        end
    end else begin
        q <= flip_flop;
        state <= flip_flop;
    end
end

endmodule
