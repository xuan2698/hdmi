module top_module (
	input clk,
	input areset,
	input x,
	output reg z
);

reg [1:0] state, next_state;
parameter INIT = 2'b00, COPY = 2'b01, COMP = 2'b10;

always @(posedge clk or posedge areset) begin
    if (areset)
        state <= INIT;
    else
        state <= next_state;
end

always @(*) begin
    case (state)
        INIT: next_state = x ? COPY : INIT;
        COPY: next_state = COMP;
        COMP: next_state = COMP;
        default: next_state = INIT;
    endcase
end

always @(*) begin
    case (state)
        INIT: z = x;
        COPY: z = x;
        COMP: z = ~x;
        default: z = x;
    endcase
end

endmodule