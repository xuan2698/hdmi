module top_module (
    input clk,
    input areset,
    input bump_left,
    input bump_right,
    input ground,
    output reg walk_left,
    output reg walk_right,
    output reg aaah
);

    typedef enum reg [1:0] {
        STATE_WALK_LEFT = 2'b00,
        STATE_WALK_RIGHT = 2'b01,
        STATE_FALL_LEFT = 2'b10,
        STATE_FALL_RIGHT = 2'b11
    } state_t;

    state_t state, next_state;

    always @(posedge clk or posedge areset) begin
        if (areset) begin
            state <= STATE_WALK_LEFT;
        end else begin
            state <= next_state;
        end
    end

    always @(*) begin
        case (state)
            STATE_WALK_LEFT: begin
                if (!ground) begin
                    next_state = STATE_FALL_LEFT;
                end else if (bump_left || bump_right) begin
                    next_state = STATE_WALK_RIGHT;
                end else begin
                    next_state = STATE_WALK_LEFT;
                end
            end
            STATE_WALK_RIGHT: begin
                if (!ground) begin
                    next_state = STATE_FALL_RIGHT;
                end else if (bump_left || bump_right) begin
                    next_state = STATE_WALK_LEFT;
                end else begin
                    next_state = STATE_WALK_RIGHT;
                end
            end
            STATE_FALL_LEFT: begin
                if (ground) begin
                    next_state = STATE_WALK_LEFT;
                end else begin
                    next_state = STATE_FALL_LEFT;
                end
            end
            STATE_FALL_RIGHT: begin
                if (ground) begin
                    next_state = STATE_WALK_RIGHT;
                end else begin
                    next_state = STATE_FALL_RIGHT;
                end
            end
            default: begin
                next_state = STATE_WALK_LEFT;
            end
        endcase
    end

    always @(*) begin
        walk_left = 0;
        walk_right = 0;
        aaah = 0;
        case (state)
            STATE_WALK_LEFT: begin
                walk_left = 1;
            end
            STATE_WALK_RIGHT: begin
                walk_right = 1;
            end
            STATE_FALL_LEFT,
            STATE_FALL_RIGHT: begin
                aaah = 1;
            end
        endcase
    end

endmodule
