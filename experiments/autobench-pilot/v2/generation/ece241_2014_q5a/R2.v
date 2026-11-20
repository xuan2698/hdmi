module top_module (
    input clk,
    input areset,
    input x,
    output reg z
);

    typedef enum reg [1:0] {
        IDLE = 2'b00,
        FLIP = 2'b01,
        PASS = 2'b10
    } state_t;

    state_t current_state, next_state;

    always @(posedge clk or posedge areset) begin
        if (areset) begin
            current_state <= IDLE;
        end else begin
            current_state <= next_state;
        end
    end

    always @(*) begin
        case (current_state)
            IDLE: begin
                if (x == 1'b1) begin
                    next_state = FLIP;
                    z = 1'b1;
                end else begin
                    next_state = PASS;
                    z = 1'b0;
                end
            end
            
            FLIP: begin
                next_state = FLIP;
                z = ~x;
            end
            
            PASS: begin
                next_state = PASS;
                z = x;
            end
            
            default: begin
                next_state = IDLE;
                z = 1'b0;
            end
        endcase
    end

endmodule
