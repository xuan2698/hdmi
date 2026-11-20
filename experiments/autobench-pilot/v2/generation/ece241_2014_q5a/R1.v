module top_module (
    input clk,
    input areset,
    input x,
    output reg z
);

    typedef enum reg [1:0] {S0, S1, S2} states_t;
    states_t state, next_state;

    always @(posedge clk or posedge areset) begin
        if (areset)
            state <= S0;
        else
            state <= next_state;
    end

    always @(*) begin
        case (state)
            S0: begin
                z = x;     // Initial state to pass input directly
                if (x == 1'b1)
                    next_state = S1;
                else
                    next_state = S0;
            end
            
            S1: begin
                z = ~x;    // Inverting the input
                if (x == 1'b1)
                    next_state = S2;
                else
                    next_state = S1;
            end
            
            S2: begin
                z = ~x;    // Continue complementing and adding one
                next_state = S2;
            end
            
            default: begin
                z = x;    // Default to avoid latches
                next_state = S0;
            end
        endcase
    end

endmodule
