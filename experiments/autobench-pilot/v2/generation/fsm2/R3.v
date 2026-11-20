module top_module (
	input clk,
	input j,
	input k,
	input areset,
	output reg out
);

    // State encoding
    typedef enum logic [1:0] {
        OFF = 1'b0,
        ON = 1'b1
    } state_t;

    state_t state, next_state;

    // Asynchronous reset and state transition
    always_ff @(posedge clk or posedge areset) begin
        if (areset) 
            state <= OFF;
        else
            state <= next_state;
    end

    // Next state logic and output logic
    always_comb begin
        case (state)
            OFF: begin
                out = 1'b0;
                if (j)
                    next_state = ON;
                else
                    next_state = OFF;
            end
            ON: begin
                out = 1'b1;
                if (k)
                    next_state = OFF;
                else
                    next_state = ON;
            end
            default: begin
                next_state = OFF;
                out = 1'b0;
            end
        endcase
    end

endmodule
