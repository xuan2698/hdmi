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

    parameter LEFT = 2'b00, RIGHT = 2'b01, FALL = 2'b10, DIG = 2'b11;
    reg [1:0] state, next_state;
    reg [4:0] fall_counter;
    reg direction;

    always @(posedge clk or posedge areset) begin
        if (areset) begin
            state <= LEFT;
            fall_counter <= 0;
            direction <= 0;
        end else begin
            state <= next_state;
            if (state == FALL) begin
                if (fall_counter < 20)
                    fall_counter <= fall_counter + 1;
            end else begin
                fall_counter <= 0;
            end
            if (state == LEFT || state == RIGHT)
                direction <= (state == LEFT) ? 0 : 1;
        end
    end

    always @(*) begin
        next_state = state;
        case (state)
            LEFT, RIGHT: begin
                if (!ground)
                    next_state = FALL;
                else if (dig)
                    next_state = DIG;
                else if ((state == LEFT && bump_left) || (state == RIGHT && bump_right))
                    next_state = (state == LEFT) ? RIGHT : LEFT;
            end
            FALL: begin
                if (ground) begin
                    if (fall_counter > 20)
                        next_state = FALL;
                    else
                        next_state = direction ? RIGHT : LEFT;
                end
            end
            DIG: begin
                if (!ground)
                    next_state = FALL;
            end
        endcase
    end

    always @(*) begin
        walk_left = (state == LEFT);
        walk_right = (state == RIGHT);
        aaah = (state == FALL);
        digging = (state == DIG);
    end

endmodule