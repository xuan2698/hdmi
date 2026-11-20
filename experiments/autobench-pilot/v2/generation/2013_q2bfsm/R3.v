module top_module (
    input clk,
    input resetn,
    input x,
    input y,
    output reg f,
    output reg g
);

    typedef enum reg [2:0] {
        STATE_A = 3'b000,
        STATE_B = 3'b001,
        STATE_C = 3'b010,
        STATE_D = 3'b011,
        STATE_E = 3'b100,
        STATE_F = 3'b101
    } state_t;

    reg [2:0] state, next_state;

    always @(posedge clk) begin
        if (!resetn)
            state <= STATE_A;
        else
            state <= next_state;
    end

    always @(*) begin
        next_state = state;  // Default state is the same unless overridden
        f = 0;
        g = 0;
        case (state)
            STATE_A: begin
                f = 0;
                if (resetn)  // If reset is de-asserted
                    next_state = STATE_B;
            end
            
            STATE_B: begin
                f = 1;
                next_state = STATE_C;
            end
            
            STATE_C: begin
                if (x == 1)
                    next_state = STATE_D;
            end
            
            STATE_D: begin
                if (x == 0)
                    next_state = STATE_E;
                else if (x != 1)
                    next_state = STATE_C;
            end
            
            STATE_E: begin
                if (x == 1) begin
                    g = 1;
                    next_state = STATE_F;
                end
                else if (x != 0)
                    next_state = STATE_C;
            end
            
            STATE_F: begin
                g = 1;
                if (y == 1)
                    g = 1;
                else if (y == 0)
                    next_state = STATE_A;
            end
        endcase
    end
endmodule
