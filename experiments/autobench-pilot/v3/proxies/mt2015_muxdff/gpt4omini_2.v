module top_module(
    input clk,
    input L,
    input q_in,
    input r_in,
    output reg Q
);
    reg [2:0] q;

    always @(posedge clk) begin
        if (L) begin
            q <= {q_in, r_in, q[2]};
        end else begin
            q <= {q[1] ^ q[2], q[0], q[2]};
        end
    end

    assign Q = q[0];
endmodule
