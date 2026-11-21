module top_module(
	input clk,
	input reset,
	input ena,
	output reg pm,
	output reg [7:0] hh,
	output reg [7:0] mm,
	output reg [7:0] ss
);

    reg [3:0] ss_ones, ss_tens;
    reg [3:0] mm_ones, mm_tens;
    reg [3:0] hh_ones, hh_tens;

    always @(posedge clk) begin
        if (reset) begin
            pm <= 0;
            hh <= 8'h12;
            mm <= 8'h00;
            ss <= 8'h00;
            ss_ones <= 4'd0;
            ss_tens <= 4'd0;
            mm_ones <= 4'd0;
            mm_tens <= 4'd0;
            hh_ones <= 4'd2;
            hh_tens <= 4'd1;
        end
        else if (ena) begin
            if (ss_ones == 4'd9) begin
                ss_ones <= 4'd0;
                if (ss_tens == 4'd5) begin
                    ss_tens <= 4'd0;
                    if (mm_ones == 4'd9) begin
                        mm_ones <= 4'd0;
                        if (mm_tens == 4'd5) begin
                            mm_tens <= 4'd0;
                            if (hh == 8'h11) begin
                                hh <= 8'h12;
                                pm <= ~pm;
                            end
                            else if (hh == 8'h12) begin
                                hh <= 8'h01;
                            end
                            else if (hh[3:0] == 4'd9) begin
                                hh <= {4'h1, 4'h0};
                            end
                            else begin
                                hh <= hh + 8'h01;
                            end
                        end
                        else begin
                            mm_tens <= mm_tens + 4'd1;
                        end
                    end
                    else begin
                        mm_ones <= mm_ones + 4'd1;
                    end
                end
                else begin
                    ss_tens <= ss_tens + 4'd1;
                end
            end
            else begin
                ss_ones <= ss_ones + 4'd1;
            end
        end
    end

    always @(*) begin
        ss = {ss_tens, ss_ones};
        mm = {mm_tens, mm_ones};
        hh = {hh_tens, hh_ones};
    end

endmodule