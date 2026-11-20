module top_module(
    input clk,
    input reset,
    output shift_ena
);

    reg [2:0] count;
    reg ena;

    assign shift_ena = ena;

    always @(posedge clk) begin
        if (reset) begin
            count <= 3'b000;
            ena <= 1;
        end else if (ena) begin
            count <= count + 1;
            if (count == 3) begin
                ena <= 0;
            end
        end
    end

endmodule
