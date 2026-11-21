module top_module (
    input clk,
    input areset,
    input bump_left,
    input bump_right,
    input ground,
    input dig,
    output walk_left,
    output walk_right,
    output aaah,
    output digging
);

    // State encoding
    typedef enum logic [2:0] {
        STATE_WALK_LEFT  = 3'b000,
        STATE_WALK_RIGHT = 3'b001,
        STATE_FALL_LEFT  = 3'b010,
        STATE_FALL_RIGHT = 3'b011,
        STATE_DIG_LEFT   = 3'b100,
        STATE_DIG_RIGHT  = 3'b101,
        STATE_SPLATTERED = 3'b111
    } state_t;

    state_t state, next_state;
    logic [4:0] fall_count;

    // State transition
    always_ff @(posedge clk or posedge areset) begin
        if (areset) begin
            state <= STATE_WALK_LEFT;
            fall_count <= 5'b0;
        end else begin
            state <= next_state;
            if (next_state == STATE_FALL_LEFT || next_state == STATE_FALL_RIGHT) begin
                fall_count <= fall_count + 1;
            end else begin
                fall_count <= 5'b0;
            end
        end
    end

    // Next state logic
    always_comb begin
        case (state)
            STATE_WALK_LEFT: begin
                if (!ground) begin
                    next_state = STATE_FALL_LEFT;
                end else if (dig) begin
                    next_state = STATE_DIG_LEFT;
                end else if (bump_left) begin
                    next_state = STATE_WALK_RIGHT;
                end else begin
                    next_state = STATE_WALK_LEFT;
                end
            end
            STATE_WALK_RIGHT: begin
                if (!ground) begin
                    next_state = STATE_FALL_RIGHT;
                end else if (dig) begin
                    next_state = STATE_DIG_RIGHT;
                end else if (bump_right) begin
                    next_state = STATE_WALK_LEFT;
                end else begin
                    next_state = STATE_WALK_RIGHT;
                end
            end
            STATE_FALL_LEFT: begin
                if (fall_count > 20) begin
                    next_state = STATE_SPLATTERED;
                end else if (ground) begin
                    next_state = STATE_WALK_LEFT;
                end else begin
                    next_state = STATE_FALL_LEFT;
                end
            end
            STATE_FALL_RIGHT: begin
                if (fall_count > 20) begin
                    next_state = STATE_SPLATTERED;
                end else if (ground) begin
                    next_state = STATE_WALK_RIGHT;
                end else begin
                    next_state = STATE_FALL_RIGHT;
                end
            end
            STATE_DIG_LEFT: begin
                if (!ground) begin
                    next_state = STATE_FALL_LEFT;
                end else begin
                    next_state = STATE_DIG_LEFT;
                end
            end
            STATE_DIG_RIGHT: begin
                if (!ground) begin
                    next_state = STATE_FALL_RIGHT;
                end else begin
                    next_state = STATE_DIG_RIGHT;
                end
            end
            STATE_SPLATTERED: begin
                next_state = STATE_SPLATTERED;
            end
            default: begin
                next_state = STATE_WALK_LEFT;
            end
        endcase
    end

    // Output logic
    assign walk_left = (state == STATE_WALK_LEFT);
    assign walk_right = (state == STATE_WALK_RIGHT);
    assign aaah = (state == STATE_FALL_LEFT || state == STATE_FALL_RIGHT);
    assign digging = (state == STATE_DIG_LEFT || state == STATE_DIG_RIGHT);

endmodule
