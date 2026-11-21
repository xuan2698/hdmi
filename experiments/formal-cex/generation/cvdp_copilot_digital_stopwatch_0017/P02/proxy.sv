module dig_stopwatch #(
    parameter CLK_FREQ = 200
) (
    input  logic       clk,
    input  logic       reset,
    input  logic       start_stop,
    output logic [5:0] seconds,
    output logic [5:0] minutes,
    output logic       hour
);

    localparam integer PERIOD = 1_000_000_000 / CLK_FREQ;

    logic [31:0] clk_cnt;
    logic        one_sec_pulse;
    logic        running;

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            clk_cnt       <= 32'd0;
            one_sec_pulse <= 1'b0;
        end else begin
            if (running) begin
                if (clk_cnt >= PERIOD - 1) begin
                    clk_cnt       <= 32'd0;
                    one_sec_pulse <= 1'b1;
                end else begin
                    clk_cnt       <= clk_cnt + 32'd1;
                    one_sec_pulse <= 1'b0;
                end
            end else begin
                clk_cnt       <= 32'd0;
                one_sec_pulse <= 1'b0;
            end
        end
    end

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            running <= 1'b0;
        end else begin
            running <= start_stop;
        end
    end

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            seconds <= 6'd0;
            minutes <= 6'd0;
            hour    <= 1'b0;
        end else if (one_sec_pulse) begin
            if (seconds >= 6'd59) begin
                seconds <= 6'd0;
                if (minutes >= 6'd59) begin
                    minutes <= 6'd0;
                    hour    <= 1'b1;
                end else begin
                    minutes <= minutes + 6'd1;
                end
            end else begin
                seconds <= seconds + 6'd1;
            end
        end
    end

endmodule
