module top_module (
    input clk,
    input a, 
    output reg [2:0] q
);

    always @(posedge clk) begin
        if (a) begin
            if (q == 3'd0) 
                q <= 3'd4;
            else if (q == 3'd1)
                q <= 3'd0;
            else
                q <= q + 1'b1;
        end
    end

    initial begin
        q = 3'd0;
    end

endmodule
