module top_module(
    input clk,
    input reset,
    output reg shift_ena
);

    reg [2:0] state;
    parameter IDLE = 3'b000;
    parameter SHIFT1 = 3'b001;
    parameter SHIFT2 = 3'b010;
    parameter SHIFT3 = 3'b011;
    parameter SHIFT4 = 3'b100;
    
    always @(posedge clk) begin
        if (reset) begin
            state <= SHIFT1;
        end else begin
            case (state)
                IDLE: begin
                    shift_ena <= 0;
                    state <= IDLE;
                end
                SHIFT1: begin
                    shift_ena <= 1;
                    state <= SHIFT2;
                end
                SHIFT2: begin
                    shift_ena <= 1;
                    state <= SHIFT3;
                end
                SHIFT3: begin
                    shift_ena <= 1;
                    state <= SHIFT4;
                end
                SHIFT4: begin
                    shift_ena <= 1;
                    state <= IDLE;
                end
                default: begin
                    shift_ena <= 0;
                    state <= IDLE;
                end
            endcase
        end
    end
endmodule
