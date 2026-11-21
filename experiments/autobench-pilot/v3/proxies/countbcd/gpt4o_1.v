module top_module(
    input clk,
    input reset,
    output [3:1] ena,
    output reg [15:0] q);

    wire[3:0] carry; // carry signals for incrementing the higher decades

    // Compute enable signals, indicating when each decade should increment
    assign ena[1] = (q[3:0] == 4'b1001); // enable tens when ones digit reaches 9
    assign ena[2] = (q[7:4] == 4'b1001) && ena[1]; // enable hundreds when tens digit reaches 9 and is enabled
    assign ena[3] = (q[11:8] == 4'b1001) && ena[2]; // enable thousands when hundreds digit reaches 9 and is enabled

    // Reset or count logic
    always @(posedge clk) begin
        if (reset) begin
            q <= 16'd0;
        end else begin
            // Count logic for each digit
            if (q[3:0] == 4'b1001) begin
                q[3:0] <= 4'b0000;
            end else begin
                q[3:0] <= q[3:0] + 1;
            end

            if (ena[1]) begin
                if (q[7:4] == 4'b1001) begin
                    q[7:4] <= 4'b0000;
                end else begin
                    q[7:4] <= q[7:4] + 1;
                end
            end

            if (ena[2]) begin
                if (q[11:8] == 4'b1001) begin
                    q[11:8] <= 4'b0000;
                end else begin
                    q[11:8] <= q[11:8] + 1;
                end
            end

            if (ena[3]) begin
                if (q[15:12] == 4'b1001) begin
                    q[15:12] <= 4'b0000;
                end else begin
                    q[15:12] <= q[15:12] + 1;
                end
            end
        end
    end

endmodule
