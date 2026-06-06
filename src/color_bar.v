//*************************************************************************
// HDMI Snake Game Display
// 1920x1080@60Hz
// KEY0: Up
// KEY1: Down
// KEY2: Left
// KEY3: Right
//*************************************************************************/

module color_bar(
    input clk,
    input rst,
    input [3:0] key,
   output reg [3:0] led,
    output reg hs,
    output reg vs,
    output reg de,
    output reg [7:0] rgb_r,
    output reg [7:0] rgb_g,
    output reg [7:0] rgb_b
);

// ======================================================
// 1080P video timing
// pixel clock = 148.5MHz
// ======================================================
parameter H_ACTIVE = 16'd1920;
parameter H_FP     = 16'd88;
parameter H_SYNC   = 16'd44;
parameter H_BP     = 16'd148;
parameter H_TOTAL  = H_ACTIVE + H_FP + H_SYNC + H_BP;

parameter V_ACTIVE = 16'd1080;
parameter V_FP     = 16'd4;
parameter V_SYNC   = 16'd5;
parameter V_BP     = 16'd36;
parameter V_TOTAL  = V_ACTIVE + V_FP + V_SYNC + V_BP;

parameter H_START  = H_FP + H_SYNC + H_BP;
parameter V_START  = V_FP + V_SYNC + V_BP;

// ======================================================
// Color define
// ======================================================
localparam [23:0] C_BLACK   = 24'h000000;
localparam [23:0] C_BG      = 24'h101018;
localparam [23:0] C_GRID    = 24'h202030;
localparam [23:0] C_HEAD    = 24'h00FF00;
localparam [23:0] C_BODY    = 24'h00AA00;
localparam [23:0] C_FOOD    = 24'hFF2020;
localparam [23:0] C_FOOTER  = 24'h000040;
localparam [23:0] C_SCORE   = 24'h00FFFF;
localparam [23:0] C_OVER_BG = 24'h400000;
localparam [23:0] C_WHITE   = 24'hFFFFFF;

// ======================================================
// Snake game parameters
// 屏幕 1920x1080
// 每个格子 32x32
// 游戏区域：60列 x 33行 = 1920 x 1056
// 底部剩余 24 像素用于分数条
// ======================================================
localparam CELL_SIZE = 32;
localparam GRID_W    = 60;
localparam GRID_H    = 33;
localparam PLAY_H    = GRID_H * CELL_SIZE;

localparam MAX_LEN   = 64;
localparam INIT_LEN  = 4;

localparam DIR_UP    = 2'd0;
localparam DIR_DOWN  = 2'd1;
localparam DIR_LEFT  = 2'd2;
localparam DIR_RIGHT = 2'd3;

// ======================================================
// Power-on reset
// ======================================================
reg [7:0] por_cnt = 8'd0;
wire por_done = (por_cnt == 8'hff);
wire sys_rst = rst | (~por_done);

always @(posedge clk or posedge rst) begin
    if (rst)
        por_cnt <= 8'd0;
    else if (!por_done)
        por_cnt <= por_cnt + 8'd1;
end

// ======================================================
// Horizontal and vertical counters
// ======================================================
reg [11:0] h_cnt;
reg [11:0] v_cnt;

wire h_end = (h_cnt == H_TOTAL - 1);
wire v_end = (v_cnt == V_TOTAL - 1);
wire frame_tick = h_end & v_end;

always @(posedge clk) begin
    if (sys_rst)
        h_cnt <= 12'd0;
    else if (h_end)
        h_cnt <= 12'd0;
    else
        h_cnt <= h_cnt + 12'd1;
end

always @(posedge clk) begin
    if (sys_rst)
        v_cnt <= 12'd0;
    else if (h_end) begin
        if (v_end)
            v_cnt <= 12'd0;
        else
            v_cnt <= v_cnt + 12'd1;
    end
end

wire video_active;
assign video_active =
    (h_cnt >= H_START) && (h_cnt < H_START + H_ACTIVE) &&
    (v_cnt >= V_START) && (v_cnt < V_START + V_ACTIVE);

wire [11:0] active_x = video_active ? (h_cnt - H_START) : 12'd0;
wire [11:0] active_y = video_active ? (v_cnt - V_START) : 12'd0;

// ======================================================
// Key sync and simple debounce
// AX7Z035B user key is active low
// key[0] : up
// key[1] : down
// key[2] : left
// key[3] : right
// ======================================================
reg [3:0] key_sync0;
reg [3:0] key_sync1;
reg [3:0] key_level;
reg [3:0] key_level_d;

always @(posedge clk) begin
    if (sys_rst) begin
        key_sync0   <= 4'b1111;
        key_sync1   <= 4'b1111;
        key_level   <= 4'b0000;
        key_level_d <= 4'b0000;
    end
    else begin
        key_sync0 <= key;
        key_sync1 <= key_sync0;

        if (frame_tick) begin
            key_level_d <= key_level;
            key_level   <= ~key_sync1;
        end
    end
end

wire key_up_press    = key_level[0] & ~key_level_d[0];
wire key_down_press  = key_level[1] & ~key_level_d[1];
wire key_left_press  = key_level[2] & ~key_level_d[2];
wire key_right_press = key_level[3] & ~key_level_d[3];

wire any_key_press = key_up_press | key_down_press | key_left_press | key_right_press;

// ======================================================
// LFSR pseudo random generator for food position
// ======================================================
reg [15:0] lfsr;

wire [5:0] rand_x_raw = lfsr[5:0];
wire [5:0] rand_y_raw = lfsr[11:6];

wire [5:0] rand_x = (rand_x_raw >= GRID_W) ? (rand_x_raw - GRID_W) : rand_x_raw;
wire [5:0] rand_y = (rand_y_raw >= GRID_H) ? (rand_y_raw - GRID_H) : rand_y_raw;

always @(posedge clk) begin
    if (sys_rst)
        lfsr <= 16'hACE1;
    else
        lfsr <= {lfsr[14:0], lfsr[15] ^ lfsr[13] ^ lfsr[12] ^ lfsr[10]};
end

// ======================================================
// Snake status
// ======================================================
reg [5:0] snake_x [0:MAX_LEN-1];
reg [5:0] snake_y [0:MAX_LEN-1];

reg [7:0] snake_len;
reg [5:0] food_x;
reg [5:0] food_y;
reg [1:0] dir;
reg game_over;
reg [7:0] score;

// Speed control
// score higher -> snake moves faster
wire [4:0] move_period =
    (score < 8'd5)  ? 5'd10 :
    (score < 8'd10) ? 5'd8  :
    (score < 8'd15) ? 5'd6  :
                      5'd4;

reg [4:0] move_frame_cnt;
reg move_tick;

always @(posedge clk) begin
    if (sys_rst) begin
        move_frame_cnt <= 5'd0;
        move_tick <= 1'b0;
    end
    else begin
        move_tick <= 1'b0;

        if (frame_tick) begin
            if (move_frame_cnt >= move_period - 1'b1) begin
                move_frame_cnt <= 5'd0;
                move_tick <= 1'b1;
            end
            else begin
                move_frame_cnt <= move_frame_cnt + 5'd1;
            end
        end
    end
end

// ======================================================
// Calculate next snake head position
// ======================================================
reg [5:0] next_head_x;
reg [5:0] next_head_y;
reg wall_hit;

always @(*) begin
    next_head_x = snake_x[0];
    next_head_y = snake_y[0];
    wall_hit = 1'b0;

    case (dir)
        DIR_UP: begin
            if (snake_y[0] == 6'd0)
                wall_hit = 1'b1;
            else
                next_head_y = snake_y[0] - 6'd1;
        end

        DIR_DOWN: begin
            if (snake_y[0] == GRID_H - 1)
                wall_hit = 1'b1;
            else
                next_head_y = snake_y[0] + 6'd1;
        end

        DIR_LEFT: begin
            if (snake_x[0] == 6'd0)
                wall_hit = 1'b1;
            else
                next_head_x = snake_x[0] - 6'd1;
        end

        DIR_RIGHT: begin
            if (snake_x[0] == GRID_W - 1)
                wall_hit = 1'b1;
            else
                next_head_x = snake_x[0] + 6'd1;
        end

        default: begin
            next_head_x = snake_x[0];
            next_head_y = snake_y[0];
        end
    endcase
end

// ======================================================
// Self collision detection
// ======================================================
integer self_i;
reg self_hit;

always @(*) begin
    self_hit = 1'b0;

    for (self_i = 1; self_i < MAX_LEN; self_i = self_i + 1) begin
        if (self_i < snake_len) begin
            if ((next_head_x == snake_x[self_i]) &&
                (next_head_y == snake_y[self_i])) begin
                self_hit = 1'b1;
            end
        end
    end
end

wire eat_food = (next_head_x == food_x) && (next_head_y == food_y);
wire grow = eat_food && (snake_len < MAX_LEN);
wire [7:0] snake_len_after = snake_len + (grow ? 8'd1 : 8'd0);

// ======================================================
// Main snake game logic
// ======================================================
integer move_i;

always @(posedge clk) begin
    if (sys_rst) begin
        snake_len <= INIT_LEN;

        snake_x[0] <= 6'd30; snake_y[0] <= 6'd16;
        snake_x[1] <= 6'd29; snake_y[1] <= 6'd16;
        snake_x[2] <= 6'd28; snake_y[2] <= 6'd16;
        snake_x[3] <= 6'd27; snake_y[3] <= 6'd16;

        for (move_i = 4; move_i < MAX_LEN; move_i = move_i + 1) begin
            snake_x[move_i] <= 6'd0;
            snake_y[move_i] <= 6'd0;
        end

        food_x <= 6'd45;
        food_y <= 6'd16;

        dir <= DIR_RIGHT;
        game_over <= 1'b0;
        score <= 8'd0;
    end
    else begin
        // Restart after game over
        if (game_over && any_key_press) begin
            snake_len <= INIT_LEN;

            snake_x[0] <= 6'd30; snake_y[0] <= 6'd16;
            snake_x[1] <= 6'd29; snake_y[1] <= 6'd16;
            snake_x[2] <= 6'd28; snake_y[2] <= 6'd16;
            snake_x[3] <= 6'd27; snake_y[3] <= 6'd16;

            for (move_i = 4; move_i < MAX_LEN; move_i = move_i + 1) begin
                snake_x[move_i] <= 6'd0;
                snake_y[move_i] <= 6'd0;
            end

            food_x <= rand_x;
            food_y <= rand_y;

            dir <= DIR_RIGHT;
            game_over <= 1'b0;
            score <= 8'd0;
        end
        else begin
            // Direction control
            // Prevent direct reverse
            if (!game_over && frame_tick) begin
                if (key_up_press && dir != DIR_DOWN)
                    dir <= DIR_UP;
                else if (key_down_press && dir != DIR_UP)
                    dir <= DIR_DOWN;
                else if (key_left_press && dir != DIR_RIGHT)
                    dir <= DIR_LEFT;
                else if (key_right_press && dir != DIR_LEFT)
                    dir <= DIR_RIGHT;
            end

            // Snake movement
            if (!game_over && move_tick) begin
                if (wall_hit || self_hit) begin
                    game_over <= 1'b1;
                end
                else begin
                    for (move_i = MAX_LEN - 1; move_i > 0; move_i = move_i - 1) begin
                        if (move_i < snake_len_after) begin
                            snake_x[move_i] <= snake_x[move_i - 1];
                            snake_y[move_i] <= snake_y[move_i - 1];
                        end
                    end

                    snake_x[0] <= next_head_x;
                    snake_y[0] <= next_head_y;

                    if (grow) begin
                        snake_len <= snake_len + 8'd1;
                        score <= score + 8'd1;

                        food_x <= rand_x;
                        food_y <= rand_y;
                    end
                end
            end
        end
    end
end
// ======================================================
// LED blink when game over
// AX7Z035B PL LED: 1 = on, 0 = off
// game_over = 1 时，4 个 LED 同时闪烁
// game_over = 0 时，4 个 LED 熄灭
// ======================================================
reg [5:0] led_frame_cnt;
reg led_blink;

always @(posedge clk) begin
    if (sys_rst) begin
        led_frame_cnt <= 6'd0;
        led_blink     <= 1'b0;
        led           <= 4'b0000;
    end
    else if (!game_over) begin
        led_frame_cnt <= 6'd0;
        led_blink     <= 1'b0;
        led           <= 4'b0000;
    end
    else begin
        if (frame_tick) begin
            if (led_frame_cnt == 6'd29) begin
                led_frame_cnt <= 6'd0;
                led_blink     <= ~led_blink;
                led           <= {4{~led_blink}};
            end
            else begin
                led_frame_cnt <= led_frame_cnt + 6'd1;
                led           <= {4{led_blink}};
            end
        end
    end
end
// ======================================================
// Convert pixel coordinate to grid coordinate
// CELL_SIZE = 32
// active_x[10:5] = active_x / 32
// active_y[10:5] = active_y / 32
// ======================================================
wire play_area   = video_active && (active_y < PLAY_H);
wire footer_area = video_active && (active_y >= PLAY_H);

wire [5:0] cell_x = active_x[10:5];
wire [5:0] cell_y = active_y[10:5];

wire [4:0] cell_px_x = active_x[4:0];
wire [4:0] cell_px_y = active_y[4:0];

wire cell_inner =
    (cell_px_x > 5'd2) && (cell_px_x < 5'd29) &&
    (cell_px_y > 5'd2) && (cell_px_y < 5'd29);

wire grid_line =
    play_area &&
    ((cell_px_x == 5'd0) || (cell_px_y == 5'd0));

wire food_area =
    play_area &&
    cell_inner &&
    (cell_x == food_x) &&
    (cell_y == food_y);

wire snake_head_area =
    play_area &&
    cell_inner &&
    (cell_x == snake_x[0]) &&
    (cell_y == snake_y[0]);

integer draw_i;
reg snake_body_area;

always @(*) begin
    snake_body_area = 1'b0;

    for (draw_i = 1; draw_i < MAX_LEN; draw_i = draw_i + 1) begin
        if (draw_i < snake_len) begin
            if ((cell_x == snake_x[draw_i]) &&
                (cell_y == snake_y[draw_i]) &&
                play_area &&
                cell_inner) begin
                snake_body_area = 1'b1;
            end
        end
    end
end

// Bottom score bar
wire [5:0] footer_cell_x = active_x[10:5];

wire score_bar_area =
    footer_area &&
    (active_y >= PLAY_H + 12'd4) &&
    (active_y <  PLAY_H + 12'd20) &&
    (footer_cell_x < score[5:0]);

// ======================================================
// Pixel color generation
// ======================================================
reg [23:0] pixel_data;

always @(*) begin
    pixel_data = C_BLACK;

    if (video_active) begin
        if (game_over) begin
            if (snake_head_area || snake_body_area)
                pixel_data = C_WHITE;
            else if (food_area)
                pixel_data = C_FOOD;
            else
                pixel_data = C_OVER_BG;
        end
        else if (food_area) begin
            pixel_data = C_FOOD;
        end
        else if (snake_head_area) begin
            pixel_data = C_HEAD;
        end
        else if (snake_body_area) begin
            pixel_data = C_BODY;
        end
        else if (score_bar_area) begin
            pixel_data = C_SCORE;
        end
        else if (footer_area) begin
            pixel_data = C_FOOTER;
        end
        else if (grid_line) begin
            pixel_data = C_GRID;
        end
        else begin
            pixel_data = C_BG;
        end
    end
end

// ======================================================
// Output sync and RGB data
// ======================================================
always @(posedge clk) begin
    if (sys_rst) begin
        hs <= 1'b0;
        vs <= 1'b0;
        de <= 1'b0;

        rgb_r <= 8'd0;
        rgb_g <= 8'd0;
        rgb_b <= 8'd0;
    end
    else begin
        hs <= (h_cnt >= H_FP) && (h_cnt < H_FP + H_SYNC);
        vs <= (v_cnt >= V_FP) && (v_cnt < V_FP + V_SYNC);
        de <= video_active;

        rgb_r <= pixel_data[23:16];
        rgb_g <= pixel_data[15:8];
        rgb_b <= pixel_data[7:0];
    end
end

endmodule