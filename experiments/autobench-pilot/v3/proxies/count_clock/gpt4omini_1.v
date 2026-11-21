module top_module(
    input clk,
    input reset,
    input ena,
    output reg pm,
    output reg [7:0] hh,
    output reg [7:0] mm,
    output reg [7:0] ss
);
    
    always @(posedge clk) begin
        if (reset) begin
            hh <= 8'b0001_0010; // 12:00 AM in BCD
            mm <= 8'b0000_0000; // 00 minutes
            ss <= 8'b0000_0000; // 00 seconds
            pm <= 1'b0;         // AM
        end else if (ena) begin
            if (ss == 8'b0101_1001) begin // 59 seconds
                ss <= 8'b0000_0000; // reset seconds
                if (mm == 8'b0101_1001) begin // 59 minutes
                    mm <= 8'b0000_0000; // reset minutes
                    if (hh == 8'b0001_0010) begin // 12 hours
                        hh <= 8'b0001_0001; // reset to 1 hour
                        pm <= ~pm; // toggle AM/PM
                    end else if (hh == 8'b0001_0001) begin // 1 hour
                        hh <= 8'b0001_0010; // set to 2 hours
                    end else if (hh == 8'b0001_0010) begin // 2 hours
                        hh <= 8'b0001_0011; // set to 3 hours
                    end else if (hh == 8'b0001_0011) begin // 3 hours
                        hh <= 8'b0001_0100; // set to 4 hours
                    end else if (hh == 8'b0001_0100) begin // 4 hours
                        hh <= 8'b0001_0101; // set to 5 hours
                    end else if (hh == 8'b0001_0101) begin // 5 hours
                        hh <= 8'b0001_0110; // set to 6 hours
                    end else if (hh == 8'b0001_0110) begin // 6 hours
                        hh <= 8'b0001_0111; // set to 7 hours
                    end else if (hh == 8'b0001_0111) begin // 7 hours
                        hh <= 8'b0001_1000; // set to 8 hours
                    end else if (hh == 8'b0001_1000) begin // 8 hours
                        hh <= 8'b0001_1001; // set to 9 hours
                    end else if (hh == 8'b0001_1001) begin // 9 hours
                        hh <= 8'b0001_1010; // set to 10 hours
                    end else if (hh == 8'b0001_1010) begin // 10 hours
                        hh <= 8'b0001_1011; // set to 11 hours
                    end else if (hh == 8'b0001_1011) begin // 11 hours
                        hh <= 8'b0001_1100; // set to 12 hours
                    end 
                end else begin
                    mm <= mm + 1; // increment minutes
                end
            end else begin
                ss <= ss + 1; // increment seconds
            end
        end
    end

endmodule
