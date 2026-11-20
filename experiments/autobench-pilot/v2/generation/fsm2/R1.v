module top_module (
    input clk,
    input j,
    input k,
    input areset,
    output reg out
);
    // State Declaration
    typedef enum reg {OFF, ON} state_t;
    state_t state, next_state;

    // State Transition Logic
    always @(*) begin
        case (state)
            OFF: begin
                if (j) next_state = ON;
                else next_state = OFF;
            end
            ON: begin
                if (k) next_state = OFF;
                else next_state = ON;
            end
            default: next_state = OFF;
        endcase
    end

    // State Flip-Flops with Asynchronous Reset
    always @(posedge clk or posedge areset) begin
        if (areset)
            state <= OFF;
        else
            state <= next_state;
    end

    // Output Logic
    always @(*) begin
        case (state)
            OFF: out = 1'b0;
            ON: out = 1'b1;
            default: out = 1'b0;
        endcase
    end

endmodule
