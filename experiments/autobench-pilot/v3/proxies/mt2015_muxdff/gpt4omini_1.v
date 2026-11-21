module top_module(
    input clk,
    input L,
    input q_in,
    input r_in,
    output reg Q
);
    
    reg [2:0] r;
    wire [2:0] q;

    // Flip-Flop
    always @(posedge clk) begin
        if (L) begin
            Q <= r_in;
        end else begin
            Q <= {Q[1] ^ Q[2], Q[0], Q[2]};
        end
    end

    // Instantiation of submodules
    full_module u1(.r(r), .L(L), .clk(clk), .q(q));
    full_module u2(.r(r), .L(L), .clk(clk), .q(q));
    full_module u3(.r(r), .L(L), .clk(clk), .q(q));

endmodule
