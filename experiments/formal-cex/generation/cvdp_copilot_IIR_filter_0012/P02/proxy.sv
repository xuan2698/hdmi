module iir_filt (
    input  logic               clk,
    input  logic               reset,
    input  logic signed [15:0] in_1,
    input  logic signed [15:0] in_2,
    input  logic signed [15:0] in_3,
    input  logic        [1:0]  filter_select,
    output logic signed [15:0] out_1,
    output logic signed [15:0] out_2,
    output logic signed [15:0] out_3
);

    logic signed [15:0] b0, b1, a1;

    always_comb begin
        case (filter_select)
            2'd0: begin b0 = 16'sd16384; b1 = 16'sd0;     a1 = 16'sd0;     end
            2'd1: begin b0 = 16'sd8192;  b1 = 16'sd8192;  a1 = 16'sd0;     end
            2'd2: begin b0 = 16'sd16384; b1 = 16'sd0;     a1 = 16'sd16384; end
            default: begin b0 = 16'sd16384; b1 = 16'sd0;  a1 = 16'sd0;     end
        endcase
    end

    logic signed [15:0] x1_d1, x2_d1, x3_d1;
    logic signed [15:0] y1_d1, y2_d1, y3_d1;

    logic signed [32:0] acc1, acc2, acc3;

    always_comb begin
        acc1 = (b0 * in_1) + (b1 * x1_d1) - (a1 * y1_d1);
        acc2 = (b0 * in_2) + (b1 * x2_d1) - (a1 * y2_d1);
        acc3 = (b0 * in_3) + (b1 * x3_d1) - (a1 * y3_d1);
    end

    function automatic logic signed [15:0] sat(input logic signed [32:0] v);
        logic signed [32:0] shifted;
        begin
            shifted = v >>> 14;
            if (shifted > 33'sd32767)
                sat = 16'sd32767;
            else if (shifted < -33'sd32768)
                sat = -16'sd32768;
            else
                sat = shifted[15:0];
        end
    endfunction

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            x1_d1 <= 16'sd0;
            x2_d1 <= 16'sd0;
            x3_d1 <= 16'sd0;
            y1_d1 <= 16'sd0;
            y2_d1 <= 16'sd0;
            y3_d1 <= 16'sd0;
            out_1 <= 16'sd0;
            out_2 <= 16'sd0;
            out_3 <= 16'sd0;
        end else begin
            x1_d1 <= in_1;
            x2_d1 <= in_2;
            x3_d1 <= in_3;
            out_1 <= sat(acc1);
            out_2 <= sat(acc2);
            out_3 <= sat(acc3);
            y1_d1 <= sat(acc1);
            y2_d1 <= sat(acc2);
            y3_d1 <= sat(acc3);
        end
    end

endmodule
