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
  
  typedef enum logic [2:0] {
    S_WALK_LEFT,
    S_WALK_RIGHT,
    S_FALL,
    S_DIG,
    S_SPLAT
  } state_t;
  
  state_t current_state, next_state;
  logic [5:0] fall_counter;

  always_ff @(posedge clk or posedge areset) begin
    if (areset) begin
      current_state <= S_WALK_LEFT;
      fall_counter <= 6'b0;
    end else begin
      current_state <= next_state;
      if (current_state == S_FALL) begin
        fall_counter <= fall_counter + 1;
      end else begin
        fall_counter <= 6'b0;
      end
    end
  end
  
  always_comb begin
    // Default outputs
    walk_left = 0;
    walk_right = 0;
    aaah = 0;
    digging = 0;
    
    case (current_state)
      S_WALK_LEFT: begin
        walk_left = 1;
        if (!ground) begin
          next_state = S_FALL;
          aaah = 1;
        end else if (dig) begin
          next_state = S_DIG;
          digging = 1;
        end else if (bump_right) begin
          next_state = S_WALK_RIGHT;
        end else if (bump_left) begin
          next_state = S_WALK_LEFT;
        end else begin
          next_state = S_WALK_LEFT;
        end
      end
      
      S_WALK_RIGHT: begin
        walk_right = 1;
        if (!ground) begin
          next_state = S_FALL;
          aaah = 1;
        end else if (dig) begin
          next_state = S_DIG;
          digging = 1;
        end else if (bump_left) begin
          next_state = S_WALK_LEFT;
        end else if (bump_right) begin
          next_state = S_WALK_RIGHT;
        end else begin
          next_state = S_WALK_RIGHT;
        end
      end
      
      S_FALL: begin
        aaah = 1;
        if (ground) begin
          if (fall_counter > 20) begin
            next_state = S_SPLAT;
          end else begin
            next_state = (walk_left ? S_WALK_LEFT : S_WALK_RIGHT);
          end
        end else begin
          next_state = S_FALL;
        end
      end
      
      S_DIG: begin
        digging = 1;
        if (!ground) begin
          next_state = S_FALL;
          aaah = 1;
        end else if (ground) begin
          next_state = (walk_left ? S_WALK_LEFT : S_WALK_RIGHT);
        end else begin
          next_state = S_DIG;
        end
      end
      
      S_SPLAT: begin
        walk_left = 0;
        walk_right = 0;
        aaah = 0;
        digging = 0;
        next_state = S_SPLAT; // Remain in splat state
      end
      
      default: begin
        next_state = S_WALK_LEFT; // default state
      end
    endcase
  end
  
endmodule
