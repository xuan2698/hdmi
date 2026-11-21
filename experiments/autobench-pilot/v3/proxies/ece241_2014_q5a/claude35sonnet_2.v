module top_module (
	input clk,
	input areset,
	input x,
	output z
);

    reg [1:0] state, next_state;
    reg z_reg;
    
    parameter INIT = 2'b00,
              COPY = 2'b01,
              FLIP = 2'b10;

    always @(posedge clk or posedge areset) begin
        if (areset)
            state <= INIT;
        else
            state <= next_state;
    end

    always @(*) begin
        case (state)
            INIT: next_state = COPY;
            COPY: next_state = (x) ? FLIP : COPY;
            FLIP: next_state = FLIP;
            default: next_state = INIT;
        endcase
    end

    always @(posedge clk or posedge areset) begin
        if (areset)
            z_reg <= 0;
        else begin
            case (state)
                INIT: z_reg <= 0;
                COPY: z_reg <= x;
                FLIP: z_reg <= ~x;
            endcase
        end
    end

    assign z = z_reg;

endmodule