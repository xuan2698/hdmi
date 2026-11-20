module top_module(
    input clk,
    input reset,
    input ena,
    output reg pm,
    output reg [7:0] hh,
    output reg [7:0] mm,
    output reg [7:0] ss);

    // Initialize hh, mm, ss, and pm
    initial begin
        hh = 8'b00010010;  // "12"
        mm = 8'b00000000;  // "00"
        ss = 8'b00000000;  // "00"
        pm = 1'b0;         // "AM"
    end

    always @(posedge clk) begin
        if (reset) begin
            // Reset clock to 12:00 AM
            hh <= 8'b00010010;
            mm <= 8'b00000000;
            ss <= 8'b00000000;
            pm <= 1'b0;
        end else if (ena) begin
            // Increment seconds
            if (ss[3:0] == 4'd9) begin
                if (ss[7:4] == 4'd5) begin
                    ss <= 8'b00000000;  // Roll over to "00"

                    // Increment minutes
                    if (mm[3:0] == 4'd9) begin
                        if (mm[7:4] == 4'd5) begin
                            mm <= 8'b00000000;  // Roll over to "00"

                            // Increment hours
                            if (hh == 8'b00010010) begin
                                hh <= 8'b00000001;  // Roll over to "01"
                                pm <= ~pm;          // Toggle AM/PM
                            end else if (hh[3:0] == 4'd9) begin
                                hh[3:0] <= 4'd0;
                                hh[7:4] <= hh[7:4] + 1;
                            end else begin
                                hh <= hh + 1;
                            end
                        end else begin
                            mm[7:4] <= mm[7:4] + 1;
                            mm[3:0] <= 4'd0;
                        end
                    end else begin
                        mm[3:0] <= mm[3:0] + 1;
                    end
                end else begin
                    ss[7:4] <= ss[7:4] + 1;
                    ss[3:0] <= 4'd0;
                end
            end else begin
                ss[3:0] <= ss[3:0] + 1;
            end
        end
    end
endmodule
