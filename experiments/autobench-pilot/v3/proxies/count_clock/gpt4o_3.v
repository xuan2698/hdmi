module top_module(
    input clk,
    input reset,
    input ena,
    output reg pm,
    output reg [7:0] hh,
    output reg [7:0] mm,
    output reg [7:0] ss
);

    // Binary Coded Decimal counter utility
    function [7:0] bcd_increment;
        input [7:0] value;
        input [3:0] max_value;
        begin
            if (value[3:0] == 4'd9) begin
                if (value[7:4] == max_value) begin
                    bcd_increment = 8'd0;
                end else begin
                    bcd_increment = {value[7:4] + 4'd1, 4'd0};
                end
            end else begin
                bcd_increment = value + 1;
            end
        end
    endfunction

    // Initialization
    initial begin
        hh = 8'd12;
        mm = 8'd0;
        ss = 8'd0;
        pm = 0;
    end

    // Clock
    always @(posedge clk) begin
        if (reset) begin
            hh <= 8'd12;
            mm <= 8'd0;
            ss <= 8'd0;
            pm <= 0;
        end else if (ena) begin
            ss <= bcd_increment(ss, 4'd5);
            
            if (ss == 8'd59) begin
                ss <= 8'd0;
                mm <= bcd_increment(mm, 4'd5);
                
                if (mm == 8'd59) begin
                    mm <= 8'd0;
                    if (hh == 8'd12) begin
                        hh <= 8'd1;
                        pm <= ~pm;
                    end else begin
                        hh <= bcd_increment(hh, 4'd1);
                        if (hh == 8'd11 && !pm) begin
                            pm <= 1;
                        end else if (hh == 8'd11 && pm) begin
                            pm <= 0;
                        end
                    end
                end
            end
        end
    end

endmodule
