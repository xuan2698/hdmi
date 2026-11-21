module top_module (
    input clk,
    input areset,
    input x,
    output reg z
);
    reg [1:0] state, next_state;
    reg [31:0] shift_reg; // Sufficient size for arbitrary length
    reg done;

    parameter IDLE = 2'b00,
              SHIFT = 2'b01,
              COMPLEMENT = 2'b10,
              DONE = 2'b11;

    always @(posedge clk or posedge areset) begin
        if (areset) begin
            state <= IDLE;
            shift_reg <= 0;
            done <= 0;
            z <= 0;
        end else begin
            state <= next_state;
            if (state == SHIFT) begin
                shift_reg <= {x, shift_reg[31:1]};
            end else if (state == COMPLEMENT) begin
                shift_reg <= ~shift_reg + 1;
            end else if (state == DONE) begin
                z <= shift_reg[0]; // Output least significant bit
            end
        end
    end

    always @(*) begin
        case (state)
            IDLE: begin
                if (!areset) begin
                    next_state = SHIFT;
                end else begin
                    next_state = IDLE;
                end
            end
            SHIFT: begin
                if (shift_reg[31:1] == 0) begin
                    next_state = COMPLEMENT;
                end else begin
                    next_state = SHIFT;
                end
            end
            COMPLEMENT: begin
                next_state = DONE;
            end
            DONE: begin
                next_state = DONE; // Wait here until reset
            end
            default: next_state = IDLE;
        endcase
    end
endmodule
