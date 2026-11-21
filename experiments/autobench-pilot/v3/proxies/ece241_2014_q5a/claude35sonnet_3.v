module top_module (
	input clk,
	input areset,
	input x,
	output z
);

reg [1:0] state, next_state;
reg z_reg;

parameter IDLE = 2'b00;
parameter COPY = 2'b01;
parameter FLIP = 2'b10;

always @(posedge clk or posedge areset) begin
    if (areset)
        state <= IDLE;
    else
        state <= next_state;
end

always @(*) begin
    case (state)
        IDLE: next_state = COPY;
        COPY: next_state = (x) ? FLIP : COPY;
        FLIP: next_state = FLIP;
        default: next_state = IDLE;
    endcase
end

always @(posedge clk or posedge areset) begin
    if (areset)
        z_reg <= 0;
    else begin
        case (state)
            IDLE: z_reg <= 0;
            COPY: z_reg <= x;
            FLIP: z_reg <= ~x;
        endcase
    end
end

assign z = z_reg;

endmodule