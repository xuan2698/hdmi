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
            hh <= 8'd12;
            mm <= 8'd0;
            ss <= 8'd0;
            pm <= 0;
        end else if (ena) begin
            if (ss < 59) begin
                ss <= ss + 1;
            end else begin
                ss <= 0;
                if (mm < 59) begin
                    mm <= mm + 1;
                end else begin
                    mm <= 0;
                    if (hh < 12) begin
                        hh <= hh + 1;
                    end else begin
                        hh <= 1;
                        pm <= ~pm;
                    end
                end
            end
        end
    end

endmodule
