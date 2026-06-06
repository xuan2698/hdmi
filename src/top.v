//////////////////////////////////////////////////////////////////////////////////
// HDMI Snake Game Top
//////////////////////////////////////////////////////////////////////////////////

module top(
    // Differential system clock
    input                    sys_clk_p,
    input                    sys_clk_n,

    // User keys, active low
    input  [3:0]             key,

    // PL LEDs
    output [3:0]             led,

    output                   hdmi_clk,
    output [23:0]            hdmi_d,
    output                   hdmi_de,
    output                   hdmi_hs,
    output                   hdmi_vs,
    inout                    hdmi_scl,
    inout                    hdmi_sda
);

wire                            video_clk;
wire                            clk_100mhz;
wire                            video_hs;
wire                            video_vs;
wire                            video_de;
wire [7:0]                      video_r;
wire [7:0]                      video_g;
wire [7:0]                      video_b;
wire                            pll_locked;
wire [9:0]                      lut_index;
wire [31:0]                     lut_data;

assign hdmi_clk = video_clk;
assign hdmi_d   = {video_r, video_g, video_b};
assign hdmi_de  = video_de;
assign hdmi_hs  = video_hs;
assign hdmi_vs  = video_vs;

// HDMI display / snake game
color_bar hdmi_color_bar(
    .clk                     (video_clk                  ),
    .rst                     (1'b0                       ),
    .key                     (key                        ),
    .led                     (led                        ),
    .hs                      (video_hs                   ),
    .vs                      (video_vs                   ),
    .de                      (video_de                   ),
    .rgb_r                   (video_r                    ),
    .rgb_g                   (video_g                    ),
    .rgb_b                   (video_b                    )
);

// Clock wizard
video_pll video_pll_m0
(
    .clk_in1_p               (sys_clk_p                  ),
    .clk_in1_n               (sys_clk_n                  ),
    .clk_out1                (video_clk                  ),
    .clk_out2                (clk_100mhz                 ),
    .locked                  (pll_locked                 )
);

// I2C master controller, configure ADV7511
i2c_config i2c_config_m0(
    .rst                     (~pll_locked                ),
    .clk                     (clk_100mhz                 ),
    .clk_div_cnt             (16'd499                    ),
    .i2c_addr_2byte          (1'b0                       ),
    .lut_index               (lut_index                  ),
    .lut_dev_addr            (lut_data[31:24]            ),
    .lut_reg_addr            (lut_data[23:8]             ),
    .lut_reg_data            (lut_data[7:0]              ),
    .error                   (                           ),
    .done                    (                           ),
    .i2c_scl                 (hdmi_scl                   ),
    .i2c_sda                 (hdmi_sda                   )
);

// ADV7511 register LUT
lut_adv7511 lut_adv7511_m0(
    .lut_index               (lut_index                  ),
    .lut_data                (lut_data                   )
);

endmodule