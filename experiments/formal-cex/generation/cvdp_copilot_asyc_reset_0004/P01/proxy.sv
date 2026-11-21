module async_reset (
    input  logic       clk,
    input  logic       reset,
    output logic [4:0] cnt_q,
    output logic       gate_clk_o,
    output logic       release_reset_o
);

    always_ff @(posedge clk or posedge reset) begin
        if (reset)
            cnt_q <= 5'h1F;
        else if (cnt_q != 5'h00)
            cnt_q <= cnt_q - 5'h01;
    end

    assign gate_clk_o      = (cnt_q > 5'h00) && (cnt_q < 5'h0E);
    assign release_reset_o = (cnt_q < 5'h08);

endmodule
