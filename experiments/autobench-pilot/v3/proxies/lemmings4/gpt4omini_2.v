module top_module (
    input clk,
    input areset,
    input bump_left,
    input bump_right,
    input ground,
    input dig,
    output reg walk_left,
    output reg walk_right,
    output reg aaah,
    output reg digging
);

    typedef enum reg [2:0] {
        WALK_LEFT,
        WALK_RIGHT,
        FALLING,
        DIGGING,
        SPLATTER
    } state_t;

    state_t current_state, next_state;
    reg [4:0] fall_counter;

    always_ff @(posedge clk or posedge areset) begin
        if (areset) begin
            current_state <= WALK_LEFT;
            fall_counter <= 0;
        end else begin
            current_state <= next_state;
            if (current_state == FALLING) begin
                fall_counter <= fall_counter + 1;
            end else begin
                fall_counter <= 0;
            end
        end
    end

    always_comb begin
        next_state = current_state;
        walk_left = 0;
        walk_right = 0;
        aaah = 0;
        digging = 0;

        case (current_state)
            WALK_LEFT: begin
                walk_left = 1;
                if (!ground) begin
                    next_state = FALLING;
                    aaah = 1;
                } else if (bump_right) begin
                    next_state = WALK_RIGHT;
                } else if (dig) begin
                    next_state = DIGGING;
                end
            end
            
            WALK_RIGHT: begin
                walk_right = 1;
                if (!ground) begin
                    next_state = FALLING;
                    aaah = 1;
                } else if (bump_left) begin
                    next_state = WALK_LEFT;
                } else if (dig) begin
                    next_state = DIGGING;
                end
            end
            
            FALLING: begin
                aaah = 1;
                if (ground) begin
                    if (fall_counter > 20) begin
                        next_state = SPLATTER;
                    end else begin
                        if (walk_left) begin
                            next_state = WALK_LEFT;
                        end else begin
                            next_state = WALK_RIGHT;
                        end
                    end
                end
            end
            
            DIGGING: begin
                digging = 1;
                if (!ground) begin
                    next_state = FALLING;
                    aaah = 1;
                end
            end
            
            SPLATTER: begin
                walk_left = 0;
                walk_right = 0;
                aaah = 0;
                digging = 0;
            end
        endcase
    end
endmodule
