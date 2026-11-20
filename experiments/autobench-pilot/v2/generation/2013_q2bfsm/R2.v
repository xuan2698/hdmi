module top_module (
    input clk,
    input resetn,
    input x,
    input y,
    output reg f,
    output reg g
);

    // Define states using a localparam for better readability
    typedef enum reg [2:0] {
        STATE_A = 3'b000,
        STATE_B = 3'b001,
        STATE_C = 3'b010,
        STATE_D = 3'b011,
        STATE_E = 3'b100,
        STATE_F = 3'b101
    } state_t;

    reg [2:0] current_state, next_state;
    reg [1:0] y_check_count; // Counter to check y for two cycles

    // Synchronous state transition
    always @(posedge clk) begin
        if (!resetn) begin
            current_state <= STATE_A;
            f <= 0;
            g <= 0;
            y_check_count <= 0;
        end else begin
            current_state <= next_state;
        end
    end

    // Next state logic and output logic
    always @(*) begin
        // Default assignments
        next_state = current_state;
        f = 0;
        g = (current_state == STATE_E) || (current_state == STATE_F);

        case (current_state)
            STATE_A: begin
                if (resetn) begin
                    next_state = STATE_B;
                    f = 1; // Set f to 1 for one cycle
                end
            end

            STATE_B: begin
                if (x) next_state = STATE_C;
            end

            STATE_C: begin
                if (!x) next_state = STATE_D;
            end

            STATE_D: begin
                if (x) next_state = STATE_E;
            end

            STATE_E: begin
                // Maintain g = 1 and start checking y
                if (y) begin
                    next_state = STATE_F;
                end else begin
                    if (y_check_count < 2) begin
                        next_state = STATE_E;
                    end else begin
                        next_state = STATE_A; // return to start if y doesn't become 1 in time
                    end
                end
            end

            STATE_F: begin
                // Stay with g = 1
            end
        endcase
    end

    // Synchronous y check counting
    always @(posedge clk) begin
        if (current_state == STATE_E) begin
            y_check_count <= y_check_count + 1;
        end else begin
            y_check_count <= 0;
        end
    end

endmodule
