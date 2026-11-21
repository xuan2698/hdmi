module top_module(
    input clk,
    input reset,
    input data,
    output reg start_shifting
);

    reg [3:0] state, next_state;

    parameter IDLE = 0, S1 = 1, S11 = 2, S110 = 3, S1101 = 4;

    always @(posedge clk) begin
        if (reset) begin
            state <= IDLE;
            start_shifting <= 0;
        end else begin
            state <= next_state;
        end
    end

    always @(*) begin
        case (state)
            IDLE: begin
                if (data) 
                    next_state = S1;
                else 
                    next_state = IDLE;
            end
            S1: begin
                if (data) 
                    next_state = S11;
                else 
                    next_state = IDLE;
            end
            S11: begin
                if (data) 
                    next_state = S110;
                else 
                    next_state = IDLE;
            end
            S110: begin
                if (data) begin
                    next_state = S1101;
                    start_shifting = 1;
                end else 
                    next_state = IDLE;
            end
            S1101: begin
                start_shifting = 1; // Remain in start_shifting state
                next_state = S1101; // Stay in this state
            end
            default: next_state = IDLE;
        endcase
    end

endmodule
