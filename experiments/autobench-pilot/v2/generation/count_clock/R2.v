module top_module(
    input clk,
    input reset,
    input ena,
    output reg pm,
    output reg [7:0] hh,
    output reg [7:0] mm,
    output reg [7:0] ss);

    always @(posedge clk) begin
        if (reset) begin
            hh <= 8'b00010010; // 12 in BCD
            mm <= 8'b00000000; // 00 in BCD
            ss <= 8'b00000000; // 00 in BCD
            pm <= 1'b0; // AM
        end else if (ena) begin
            // Increment seconds
            if (ss == 8'b01011001) begin // 59 in BCD
                ss <= 8'b00000000; // Reset seconds to 00
                // Increment minutes
                if (mm == 8'b01011001) begin // 59 in BCD
                    mm <= 8'b00000000; // Reset minutes to 00
                    // Increment hours
                    if (hh == 8'b00010010) begin // 12 in BCD
                        hh <= 8'b00000001; // Reset hours to 01
                        pm <= ~pm; // Toggle AM/PM
                    end else if (hh == 8'b00001001) begin // 9 in BCD
                        hh <= hh + 8'b00000110; // Adjust to 10
                    end else begin
                        hh <= hh + 8'b00000001; // Simple increment
                    end
                end else if (mm[3:0] == 4'b1001) begin // Last digit is 9
                    mm <= mm + 8'b00000110; // Adjust the tens digit
                end else begin
                    mm <= mm + 8'b00000001; // Simple increment
                end
            end else if (ss[3:0] == 4'b1001) begin // Last digit is 9
                ss <= ss + 8'b00000110; // Adjust the tens digit
            end else begin
                ss <= ss + 8'b00000001; // Simple increment
            end
        end
    end

endmodule
