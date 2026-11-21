module top_module (
    input clk,
    input areset,
    input x,
    output reg z
);

    reg [31:0] num; // Register to store the input number
    reg [31:0] complement; // Register to store the 2's complement
    reg [5:0] count; // Counter to keep track of input bits

    always @(posedge clk or posedge areset) begin
        if (areset) begin
            num <= 0;
            complement <= 0;
            count <= 0;
            z <= 0;
        end else begin
            if (count < 32) begin
                num <= {x, num[31:1]}; // Shift in the new bit
                count <= count + 1;
            end else begin
                complement <= ~num + 1; // Calculate 2's complement
                z <= complement[0]; // Output the least significant bit
            end
        end
    end

endmodule
