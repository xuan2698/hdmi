module top_module(
    input clk,
    input reset,
    input data,
    output reg start_shifting );

    // State encoding
    typedef enum reg [2:0] {
        IDLE = 3'b000,
        S1   = 3'b001,
        S11  = 3'b010,
        S110 = 3'b011,
        S1101 = 3'b100
    } state_t;

    state_t state, next_state;

    // State transition
    always @(posedge clk) begin
        if (reset)
            state <= IDLE;
        else
            state <= next_state;
    end

    // Next state logic
    always @(*) begin
        next_state = state; // Default to stay in the same state
        case (state)
            IDLE: 
                if (data) next_state = S1;
            S1: 
                if (data) next_state = S11;
                else next_state = IDLE;
            S11:
                if (!data) next_state = S110;
            S110:
                if (data) next_state = S1101;
                else next_state = IDLE;
            S1101: 
                next_state = S1101; // Stay in the same state
        endcase
    end

    // Output logic
    always @(posedge clk) begin
        if (reset)
            start_shifting <= 0;
        else if (state == S1101)
            start_shifting <= 1;
    end
endmodule
