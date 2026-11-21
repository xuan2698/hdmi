module top_module(
	input clk,
	input reset,
	input data,
	output reg start_shifting
);

    reg [2:0] state, next_state;
    parameter S0 = 3'b000, S1 = 3'b001, S11 = 3'b010, S110 = 3'b011, S1101 = 3'b100;

    always @(posedge clk) begin
        if (reset) begin
            state <= S0;
            start_shifting <= 0;
        end else begin
            state <= next_state;
            if (state == S1101)
                start_shifting <= 1;
        end
    end

    always @(*) begin
        case (state)
            S0: next_state = data ? S1 : S0;
            S1: next_state = data ? S11 : S0;
            S11: next_state = data ? S11 : S110;
            S110: next_state = data ? S1101 : S0;
            S1101: next_state = S1101;
            default: next_state = S0;
        endcase
    end

endmodule