module top_module(
    input clk,
    input L,
    input q_in,
    input r_in,
    output reg Q
);
    reg [2:0] q;
    wire [2:0] r = {r_in, q_in, q[2]};
    wire mux_out;

    // 2-to-1 Multiplexer
    assign mux_out = L ? r : {q[1] ^ q[2], q[0], q[2]};

    // Flip-Flop
    always @(posedge clk) begin
        Q <= mux_out;
        q <= mux_out;
    end
endmodule
