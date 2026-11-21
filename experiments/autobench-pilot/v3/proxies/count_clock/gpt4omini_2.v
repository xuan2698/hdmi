module top_module(
    input clk,
    input reset,
    input ena,
    output reg pm,
    output reg [7:0] hh,
    output reg [7:0] mm,
    output reg [7:0] ss
);

    // Initialize the clock
    initial begin
        hh = 8'b00001100; // Initial hour: 12
        mm = 8'b00000000; // Initial minutes: 00
        ss = 8'b00000000; // Initial seconds: 00
        pm = 1'b0;        // Initial state: AM
    end

    always @(posedge clk) begin
        if (reset) begin
            hh <= 8'b00001100; // Reset to 12
            mm <= 8'b00000000; // Reset to 00
            ss <= 8'b00000000; // Reset to 00
            pm <= 1'b0;        // Reset to AM
        end else if (ena) begin
            // Increment seconds
            if (ss == 8'b00111001) begin // 59 in decimal
                ss <= 8'b00000000; // Reset seconds
                // Increment minutes
                if (mm == 8'b00111001) begin // 59 in decimal
                    mm <= 8'b00000000; // Reset minutes
                    // Increment hours
                    if (hh == 8'b00001100) begin // 12 in decimal
                        hh <= 8'b00000001; // Set to 1
                        pm <= ~pm; // Toggle AM/PM
                    end else if (hh == 8'b00000001 && pm == 1'b1) begin // Transition from 1 PM to 2 PM
                        hh <= 8'b00000010; // Set to 2
                    end else if (hh < 8'b00001100) begin
                        hh <= hh + 1; // Increment hour
                    end
                end else begin
                    mm <= mm + 1; // Increment minutes
                end
            end else begin
                ss <= ss + 1; // Increment seconds
            end
        end
    end
endmodule
