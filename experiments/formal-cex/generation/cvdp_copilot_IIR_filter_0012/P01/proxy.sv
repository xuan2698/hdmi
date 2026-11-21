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

    logic signed [15:0] x1_1, x2_1, y1_1, y2_1;
    logic signed [15:0] x1_2, x2_2, y1_2, y2_2;
    logic signed [15:0] x1_3, x2_3, y1_3, y2_3;

    logic signed [15:0] b0, b1, b2, a1, a2;

    always_comb begin
        case (filter_select)
            2'd0: begin
                b0 = 16'sd8192;  b1 = 16'sd16384; b2 = 16'sd8192;
                a1 = -16'sd16384; a2 = 16'sd8192;
            end
            2'd1: begin
                b0 = 16'sd4096;  b1 = 16'sd8192;  b2 = 16'sd4096;
                a1 = -16'sd24576; a2 = 16'sd8192;
            end
            2'd2: begin
                b0 = 16'sd16384; b1 = 16'sd0;     b2 = -16'sd16384;
                a1 = -16'sd16384; a2 = 16'sd8192;
            end
            default: begin
                b0 = 16'sd8192;  b1 = 16'sd0;     b2 = -16'sd8192;
                a1 = -16'sd16384; a2 = 16'sd8192;
            end
        endcase
    end

    function automatic logic signed [15:0] sat16(input logic signed [31:0] v);
        if (v > 32'sd32767)
            sat16 = 16'sd32767;
        else if (v < -32'sd32768)
            sat16 = -16'sd32768;
        else
            sat16 = v[15:0];
    endfunction

    logic signed [31:0] acc1, acc2, acc3;

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            x1_1 <= 16'sd0; x2_1 <= 16'sd0; y1_1 <= 16'sd0; y2_1 <= 16'sd0;
            x1_2 <= 16'sd0; x2_2 <= 16'sd0; y1_2 <= 16'sd0; y2_2 <= 16'sd0;
            x1_3 <= 16'sd0; x2_3 <= 16'sd0; y1_3 <= 16'sd0; y2_3 <= 16'sd0;
            out_1 <= 16'sd0;
            out_2 <= 16'sd0;
            out_3 <= 16'sd0;
        end else begin
            acc1 = (b0 * in_1) + (b1 * x1_1) + (b2 * x2_1) - (a1 * y1_1) - (a2 * y2_1);
            acc2 = (b0 * in_2) + (b1 * x1_2) + (b2 * x2_2) - (a1 * y1_2) - (a2 * y2_2);
            acc3 = (b0 * in_3) + (b1 * x1_3) + (b2 * x2_3) - (a1 * y1_3) - (a2 * y2_3);

            out_1 <= sat16(acc1 >>> 15);
            out_2 <= sat16(acc2 >>> 15);
            out_3 <= sat16(acc3 >>> 15);

            x2_1 <= x1_1; x1_1 <= in_1;
            x2_2 <= x1_2; x1_2 <= in_2;
            x2_3 <= x1_3; x1_3 <= in_3;

            y2_1 <= y1_1; y1_1 <= sat16(acc1 >>> 15);
            y2_2 <= y1_2; y1_2 <= sat16(acc2 >>> 15);
            y2_3 <= y1_3; y1_3 <= sat16(acc3 >>> 15);
        end
    end

endmodule
