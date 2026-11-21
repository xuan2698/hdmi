module dig_stopwatch #(
    parameter int CLK_FREQ = 200
) (
    input  logic       clk,
    input  logic       reset,
    input  logic       start_stop,
    output logic [5:0] seconds,
    output logic [5:0] minutes,
    output logic       hour
);

    localparam int PERIOD = 1_000_000_000 / CLK_FREQ;

    logic [$clog2(PERIOD)-1:0] div_cnt;
    logic one_sec_pulse;

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            div_cnt <= '0;
            one_sec_pulse <= 1'b0;
        end else begin
            if (div_cnt == PERIOD[$clog2(PERIOD)-1:0] - 1) begin
                div_cnt <= '0;
                one_sec_pulse <= 1'b1;
            end else begin
                div_cnt <= div_cnt + 1'b1;
                one_sec_pulse <= 1'b0;
            end
        end
    end

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            seconds <= 6'd0;
            minutes <= 6'd0;
            hour    <= 1'b0;
        end else if (start_stop && one_sec_pulse) begin
            if (seconds == 6'd59) begin
                seconds <= 6'd0;
                if (minutes == 6'd59) begin
                    minutes <= 6'd0;
                    hour    <= 1'b1;
                end else begin
                    minutes <= minutes + 1'b1;
                end
            end else begin
                seconds <= seconds + 1'b1;
            end
        end
    end

endmodule
