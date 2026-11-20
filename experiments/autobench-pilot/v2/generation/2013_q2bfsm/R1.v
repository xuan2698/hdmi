module top_module (
    input clk,
    input resetn,
    input x,
    input y,
    output reg f,
    output reg g
);

    // State Encoding
    typedef enum reg [2:0] {
        STATE_A,
        STATE_B,
        STATE_C,
        STATE_D,
        STATE_E,
        STATE_F,
        STATE_G
    } state_t;

    state_t current_state, next_state;

    // FSM Sequential block
    always @(posedge clk or negedge resetn) begin
        if (!resetn)
            current_state <= STATE_A;
        else
            current_state <= next_state;
    end

    // FSM Combinational block
    always @(*) begin
        // Default state transitions
        next_state = current_state;
        f = 0;
        g = 0;

        case (current_state)
            STATE_A: begin
                if (!resetn) begin
                    next_state = STATE_A;
                end else begin
                    f = 1;
                    next_state = STATE_B;
                end
            end
            STATE_B: begin
                if (x) begin
                    next_state = STATE_C;
                end else begin
                    next_state = STATE_B;
                end
            end
            STATE_C: begin
                if (!x) begin
                    next_state = STATE_D;
                end else begin
                    next_state = STATE_B;
                end
            end
            STATE_D: begin
                if (x) begin
                    next_state = STATE_E;
                end else begin
                    next_state = STATE_B;
                end
            end
            STATE_E: begin
                g = 1;
                next_state = STATE_F;
            end
            STATE_F: begin
                g = 1;
                if (y) begin
                    next_state = STATE_G;
                end else begin
                    next_state = STATE_F;
                end
            end
            STATE_G: begin
                g = 1;
                // Permanent state until reset
                next_state = STATE_G;
            end
            default: next_state = STATE_A;
        endcase
    end

endmodule
