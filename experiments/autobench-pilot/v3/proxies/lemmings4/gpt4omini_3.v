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

	// State encoding
	typedef enum reg [2:0] {
		WALK_LEFT = 3'b000,
		WALK_RIGHT = 3'b001,
		FALLING = 3'b010,
		DIGGING = 3'b011,
		SPLATTER = 3'b100
	} state_t;

	state_t current_state, next_state;
	reg [4:0] fall_counter;

	always @(posedge clk or posedge areset) begin
		if (areset) begin
			current_state <= WALK_LEFT;
			fall_counter <= 5'b0;
		end else begin
			current_state <= next_state;
		end
	end

	always @(*) begin
		// Default outputs
		walk_left = 0;
		walk_right = 0;
		aaah = 0;
		digging = 0;

		// Next state logic
		case (current_state)
			WALK_LEFT: begin
				if (!ground) begin
					next_state = FALLING;
					aaah = 1;
					fall_counter = 0;
				end else if (dig) begin
					next_state = DIGGING;
					digging = 1;
				end else if (bump_right) begin
					next_state = WALK_RIGHT;
					walk_right = 1;
				end else begin
					next_state = WALK_LEFT;
					walk_left = 1;
				end
			end

			WALK_RIGHT: begin
				if (!ground) begin
					next_state = FALLING;
					aaah = 1;
					fall_counter = 0;
				end else if (dig) begin
					next_state = DIGGING;
					digging = 1;
				end else if (bump_left) begin
					next_state = WALK_LEFT;
					walk_left = 1;
				end else begin
					next_state = WALK_RIGHT;
					walk_right = 1;
				end
			end

			FALLING: begin
				if (fall_counter >= 20 && ground) begin
					next_state = SPLATTER;
				end else if (ground) begin
					next_state = (bump_left) ? WALK_RIGHT : 
					(bump_right) ? WALK_LEFT : (current_state == FALLING) ? current_state : 
					(current_state == WALK_LEFT) ? WALK_LEFT : WALK_RIGHT;
					if (next_state == WALK_LEFT) walk_left = 1;
					else if (next_state == WALK_RIGHT) walk_right = 1;
				end else begin
					next_state = FALLING;
					fall_counter = fall_counter + 1;
				end
			end

			DIGGING: begin
				if (!ground) begin
					next_state = FALLING;
					aaah = 1;
					fall_counter = 0;
				end else begin
					next_state = DIGGING;
					digging = 1;
				end
			end

			SPLATTER: begin
				next_state = SPLATTER;
				walk_left = 0;
				walk_right = 0;
				aaah = 0;
				digging = 0;
			end

			default: next_state = WALK_LEFT;
		endcase
	end
endmodule
