module top_module(
    input clk,
    input reset,
    input data,
    output reg start_shifting);

    // State encoding
    typedef enum logic [2:0] {
        S0 = 3'b000, // Initial state
        S1 = 3'b001, // Detected 1
        S2 = 3'b010, // Detected 11
        S3 = 3'b011, // Detected 110
        S4 = 3'b100  // Detected 1101, set start_shifting
    } state_t;

    state_t current_state, next_state;

    // State transition logic
    always @(posedge clk) begin
        if (reset) begin
            current_state <= S0;
            start_shifting <= 0;
        end else begin
            current_state <= next_state;
        end
    end

    // Next state and output logic
    always @(*) begin
        next_state = current_state; // Default state is current state
        case (current_state)
            S0: begin
                if (data) next_state = S1;
            end
            S1: begin
                if (data) next_state = S2;
                else next_state = S0;
            end
            S2: begin
                if (data) next_state = S2;
                else next_state = S3;
            end
            S3: begin
                if (data) next_state = S4;
                else next_state = S0;
            end
            S4: begin
                // Remain in state S4 once reached
            end
            default: next_state = S0;
        endcase
    end

    // Output logic for start_shifting
    always @(posedge clk) begin
        if (reset) begin
            start_shifting <= 0;
        end else if (next_state == S4) begin
            start_shifting <= 1;
        end
    end
endmodule
