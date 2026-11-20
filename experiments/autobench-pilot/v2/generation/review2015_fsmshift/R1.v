module top_module(
    input clk,
    input reset,
    output reg shift_ena
);

    reg [2:0] count; // 3-bit counter to count clock cycles

    always @(posedge clk) begin
        if (reset) begin
            shift_ena <= 1'b1; // Enable shift for 4 cycles
            count <= 3'b000; // Reset counter
        end else if (count < 3'b100) begin
            shift_ena <= 1'b1; // Continue enabling shift
            count <= count + 1'b1; // Increment counter
        end else begin
            shift_ena <= 1'b0; // Disable shift
        end
    end

endmodule
