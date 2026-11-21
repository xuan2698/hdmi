module top_module(
	input clk,
	input L,
	input q_in,
	input r_in,
	output reg Q);

    wire mux_out;

    // 2-1 Multiplexer
    assign mux_out = L ? r_in : q_in;

    // D Flip-Flop
    always @(posedge clk) begin
        Q <= mux_out;
    end

endmodule