module top_module(
	input clk,
	input reset,
	input data,
	output reg start_shifting
);

    reg [3:0] state;
    parameter S0 = 4'b0000,
              S1 = 4'b0001,
              S11 = 4'b0010,
              S110 = 4'b0011,
              S1101 = 4'b0100;

    always @(posedge clk) begin
        if (reset) begin
            state <= S0;
            start_shifting <= 0;
        end else begin
            case (state)
                S0: state <= data ? S1 : S0;
                S1: state <= data ? S11 : S0;
                S11: state <= data ? S11 : S110;
                S110: state <= data ? S1101 : S0;
                S1101: state <= S1101;
                default: state <= S0;
            endcase

            if (state == S1101)
                start_shifting <= 1;
        end
    end

endmodule