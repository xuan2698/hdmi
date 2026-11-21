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
    logic signed [15:0] x1_1, x1_2, x1_3;
    logic signed [15:0] y1_1, y1_2, y1_3;
    logic signed [31:0] acc1, acc2, acc3;

    always_comb begin
        case (filter_select)
            2'd0: begin b0 = 16'sd16384; b1 = 16'sd0;     a1 = 16'sd0;     end
            2'd1: begin b0 = 16'sd8192;  b1 = 16'sd8192;  a1 = 16'sd0;     end
            2'd2: begin b0 = 16'sd16384; b1 = 16'sd0;     a1 = 16'sd16384; end
            default: begin b0 = 16'sd10922; b1 = 16'sd10922; a1 = 16'sd10922; end
        endcase
    end

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            x1_1 <= 16'sd0;
            x1_2 <= 16'sd0;
            x1_3 <= 16'sd0;
            y1_1 <= 16'sd0;
            y1_2 <= 16'sd0;
            y1_3 <= 16'sd0;
            out_1 <= 16'sd0;
            out_2 <= 16'sd0;
            out_3 <= 16'sd0;
        end else begin
            x1_1 <= in_1;
            x1_2 <= in_2;
            x1_3 <= in_3;

            acc1 = (b0 * in_1) + (b1 * x1_1) - (a1 * y1_1);
            acc2 = (b0 * in_2) + (b1 * x1_2) - (a1 * y1_2);
            acc3 = (b0 * in_3) + (b1 * x1_3) - (a1 * y1_3);

            if (acc1 > 32'sd32767)       out_1 <= 16'sd32767;
            else if (acc1 < -32'sd32768) out_1 <= -16'sd32768;
            else                         out_1 <= acc1[15:0];

            if (acc2 > 32'sd32767)       out_2 <= 16'sd32767;
            else if (acc2 < -32'sd32768) out_2 <= -16'sd32768;
            else                         out_2 <= acc2[15:0];

            if (acc3 > 32'sd32767)       out_3 <= 16'sd32767;
            else if (acc3 < -32'sd32768) out_3 <= -16'sd32768;
            else                         out_3 <= acc3[15:0];

            y1_1 <= out_1;
            y1_2 <= out_2;
            y1_3 <= out_3;
        end
    end

endmodule
