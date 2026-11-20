module flipflop_mux(
    input clk,
    input L,
    input q_in,
    input r_in,
    output reg q_out
);
    always @(posedge clk) begin
        if (L) begin
            q_out <= r_in;
        end else begin
            q_out <= q_in;
        end
    end
endmodule

module top_module(
    input clk,
    input L,
    input [2:0] r_in,
    output [2:0] Q
);
    wire [2:0] q_feedback;

    flipflop_mux ffm0(
        .clk(clk),
        .L(L),
        .q_in(q_feedback[1] ^ q_feedback[2]),
        .r_in(r_in[0]),
        .q_out(q_feedback[0])
    );

    flipflop_mux ffm1(
        .clk(clk),
        .L(L),
        .q_in(q_feedback[0]),
        .r_in(r_in[1]),
        .q_out(q_feedback[1])
    );

    flipflop_mux ffm2(
        .clk(clk),
        .L(L),
        .q_in(q_feedback[2]),
        .r_in(r_in[2]),
        .q_out(q_feedback[2])
    );

    assign Q = q_feedback;
endmodule
