module top_module (
	input clk,
	input areset,
	input x,
	output reg z
);

    // State encoding
    typedef enum reg [1:0] {
        IDLE = 2'b00,
        FLIP = 2'b01,
        PASS = 2'b10
    } state_t;
    
    state_t state, next_state;
    reg flip;

    always @(posedge clk or posedge areset) begin
        if (areset) begin
            state <= IDLE;
            z <= 0;
            flip <= 0;
        end else begin
            state <= next_state;
            if (state == FLIP) begin
                z <= ~x;
                flip <= 1;
            end else if (state == PASS && flip) begin
                z <= ~x;
            end else begin
                z <= x;
            end
        end
    end

    always @(*) begin
        case (state)
            IDLE: begin
                if (~areset)
                    next_state = FLIP;
                else
                    next_state = IDLE;
            end
            FLIP: begin
                next_state = PASS;
            end
            PASS: begin
                next_state = PASS;
            end
            default: next_state = IDLE;
        endcase
    end

endmodule
