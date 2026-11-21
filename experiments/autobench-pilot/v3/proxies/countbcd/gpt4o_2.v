module top_module(
    input clk,
    input reset,
    output [3:1] ena,
    output reg [15:0] q);

    // Internal signals for enable signals
    wire ena1, ena2, ena3;
    
    // Assign enable conditions for each BCD digit
    assign ena1 = (q[3:0] == 4'd9);        // When ones digit reaches 9, tens digit enable
    assign ena2 = (q[7:4] == 4'd9) & ena1; // When tens digit reaches 9 and ones digit is at 9, hundreds digit enable
    assign ena3 = (q[11:8] == 4'd9) & ena2;// When hundreds digit reaches 9 and previous digits are maxed, thousands digit enable
    
    // Assign calculated enable signals
    assign ena = {ena3, ena2, ena1};

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            q <= 16'b0; // Reset all digits to 0
        end
        else begin
            if (ena1) begin
                q[3:0] <= 4'b0; // Reset ones digit
                if (ena2) begin
                    q[7:4] <= 4'b0; // Reset tens digit
                    if (ena3) begin
                        q[11:8] <= 4'b0; // Reset hundreds digit
                        q[15:12] <= q[15:12] + 4'b1; // Increment thousands digit
                    end
                    else begin
                        q[11:8] <= q[11:8] + 4'b1; // Increment hundreds digit
                    end
                end
                else begin
                    q[7:4] <= q[7:4] + 4'b1; // Increment tens digit
                end
            end
            else begin
                q[3:0] <= q[3:0] + 4'b1; // Increment ones digit
            end
        end
    end

endmodule
