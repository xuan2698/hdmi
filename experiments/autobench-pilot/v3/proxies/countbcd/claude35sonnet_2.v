module top_module(
	input clk,
	input reset,
	output [3:1] ena,
	output reg [15:0] q
);

    reg [3:0] digit0, digit1, digit2, digit3;

    always @(posedge clk) begin
        if (reset) begin
            digit0 <= 4'd0;
            digit1 <= 4'd0;
            digit2 <= 4'd0;
            digit3 <= 4'd0;
        end else begin
            if (digit0 == 4'd9) begin
                digit0 <= 4'd0;
                if (digit1 == 4'd9) begin
                    digit1 <= 4'd0;
                    if (digit2 == 4'd9) begin
                        digit2 <= 4'd0;
                        if (digit3 == 4'd9) begin
                            digit3 <= 4'd0;
                        end else begin
                            digit3 <= digit3 + 1;
                        end
                    end else begin
                        digit2 <= digit2 + 1;
                    end
                end else begin
                    digit1 <= digit1 + 1;
                end
            end else begin
                digit0 <= digit0 + 1;
            end
        end
    end

    assign ena[1] = (digit0 == 4'd9);
    assign ena[2] = (digit0 == 4'd9) && (digit1 == 4'd9);
    assign ena[3] = (digit0 == 4'd9) && (digit1 == 4'd9) && (digit2 == 4'd9);

    always @(*) begin
        q = {digit3, digit2, digit1, digit0};
    end

endmodule