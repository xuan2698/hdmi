module top_module(
    input clk,
    input reset,
    output [3:1] ena,
    output reg [15:0] q
);

    reg [3:0] ones, tens, hundreds, thousands;

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            ones <= 4'b0000;
            tens <= 4'b0000;
            hundreds <= 4'b0000;
            thousands <= 4'b0000;
        end else begin
            if (ones == 4'b1001) begin
                ones <= 4'b0000;
                if (tens == 4'b1001) begin
                    tens <= 4'b0000;
                    if (hundreds == 4'b1001) begin
                        hundreds <= 4'b0000;
                        if (thousands == 4'b1001) begin
                            thousands <= 4'b0000;
                        end else begin
                            thousands <= thousands + 1;
                        end
                    end else begin
                        hundreds <= hundreds + 1;
                    end
                end else begin
                    tens <= tens + 1;
                end
            end else begin
                ones <= ones + 1;
            end
        end
    end

    always @* begin
        q = {thousands, hundreds, tens, ones};
        ena[1] = (ones == 4'b1001);
        ena[2] = (tens == 4'b1001 && ones == 4'b1001);
        ena[3] = (hundreds == 4'b1001 && tens == 4'b1001 && ones == 4'b1001);
    end

endmodule
