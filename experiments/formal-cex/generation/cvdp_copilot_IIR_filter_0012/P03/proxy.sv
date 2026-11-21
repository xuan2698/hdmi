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

    logic signed [15:0] x1_d1, x1_d2;
    logic signed [15:0] x2_d1, x2_d2;
    logic signed [15:0] x3_d1, x3_d2;
    logic signed [15:0] y1_d1, y1_d2;
    logic signed [15:0] y2_d1, y2_d2;
    logic signed [15:0] y3_d1, y3_d2;

    logic signed [3:0] b0, b1, b2;
    logic signed [3:0] a1, a2;

    always_comb begin
        case (filter_select)
            2'd0: begin b0 = 4'sd1; b1 = 4'sd0; b2 = 4'sd0; a1 = 4'sd0; a2 = 4'sd0; end
            2'd1: begin b0 = 4'sd1; b1 = 4'sd1; b2 = 4'sd0; a1 = 4'sd0; a2 = 4'sd0; end
            2'd2: begin b0 = 4'sd1; b1 = 4'sd1; b2 = 4'sd1; a1 = 4'sd1; a2 = 4'sd0; end
            2'd3: begin b0 = 4'sd1; b1 = 4'sd1; b2 = 4'sd1; a1 = 4'sd1; a2 = 4'sd1; end
            default: begin b0 = 4'sd1; b1 = 4'sd0; b2 = 4'sd0; a1 = 4'sd0; a2 = 4'sd0; end
        endcase
    end

    function automatic logic signed [15:0] sat16(input logic signed [31:0] v);
        if (v > 32'sd32767)
            sat16 = 16'sh7FFF;
        else if (v < -32'sd32768)
            sat16 = 16'sh8000;
        else
            sat16 = v[15:0];
    endfunction

    logic signed [31:0] acc1, acc2, acc3;
    logic signed [15:0] y1_n, y2_n, y3_n;

    always_comb begin
        acc1 = $signed(b0) * $signed(in_1)
             + $signed(b1) * $signed(x1_d1)
             + $signed(b2) * $signed(x1_d2)
             - $signed(a1) * $signed(y1_d1)
             - $signed(a2) * $signed(y1_d2);
        acc2 = $signed(b0) * $signed(in_2)
             + $signed(b1) * $signed(x2_d1)
             + $signed(b2) * $signed(x2_d2)
             - $signed(a1) * $signed(y2_d1)
             - $signed(a2) * $signed(y2_d2);
        acc3 = $signed(b0) * $signed(in_3)
             + $signed(b1) * $signed(x3_d1)
             + $signed(b2) * $signed(x3_d2)
             - $signed(a1) * $signed(y3_d1)
             - $signed(a2) * $signed(y3_d2);
        y1_n = sat16(acc1);
        y2_n = sat16(acc2);
        y3_n = sat16(acc3);
    end

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            x1_d1 <= 16'sd0; x1_d2 <= 16'sd0;
            x2_d1 <= 16'sd0; x2_d2 <= 16'sd0;
            x3_d1 <= 16'sd0; x3_d2 <= 16'sd0;
            y1_d1 <= 16'sd0; y1_d2 <= 16'sd0;
            y2_d1 <= 16'sd0; y2_d2 <= 16'sd0;
            y3_d1 <= 16'sd0; y3_d2 <= 16'sd0;
            out_1 <= 16'sd0;
            out_2 <= 16'sd0;
            out_3 <= 16'sd0;
        end else begin
            x1_d1 <= in_1; x1_d2 <= x1_d1;
            x2_d1 <= in_2; x2_d2 <= x2_d1;
            x3_d1 <= in_3; x3_d2 <= x3_d1;
            y1_d1 <= y1_n; y1_d2 <= y1_d1;
            y2_d1 <= y2_n; y2_d2 <= y2_d1;
            y3_d1 <= y3_n; y3_d2 <= y3_d1;
            out_1 <= y1_n;
            out_2 <= y2_n;
            out_3 <= y3_n;
        end
    end

endmodule
