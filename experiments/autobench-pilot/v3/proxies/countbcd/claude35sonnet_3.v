module top_module(
	input clk,
	input reset,
	output [3:1] ena,
	output reg [15:0] q);

    wire [3:0] ena_internal;

    always @(posedge clk) begin
        if (reset) begin
            q <= 16'b0;
        end else begin
            if (ena_internal[0]) begin
                if (q[3:0] == 4'd9) q[3:0] <= 4'd0;
                else q[3:0] <= q[3:0] + 1'd1;
            end
            if (ena_internal[1]) begin
                if (q[7:4] == 4'd9) q[7:4] <= 4'd0;
                else q[7:4] <= q[7:4] + 1'd1;
            end
            if (ena_internal[2]) begin
                if (q[11:8] == 4'd9) q[11:8] <= 4'd0;
                else q[11:8] <= q[11:8] + 1'd1;
            end
            if (ena_internal[3]) begin
                if (q[15:12] == 4'd9) q[15:12] <= 4'd0;
                else q[15:12] <= q[15:12] + 1'd1;
            end
        end
    end

    assign ena_internal[0] = 1'b1;
    assign ena_internal[1] = (q[3:0] == 4'd9);
    assign ena_internal[2] = (q[7:4] == 4'd9) & ena_internal[1];
    assign ena_internal[3] = (q[11:8] == 4'd9) & ena_internal[2];

    assign ena = ena_internal[3:1];

endmodule