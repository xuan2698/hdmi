module top_module(
    input clk,
    input reset,
    input data,
    output reg start_shifting
);

    typedef enum reg [2:0] {
        STATE_IDLE = 3'b000,
        STATE_1    = 3'b001,
        STATE_11   = 3'b010,
        STATE_110  = 3'b011,
        STATE_1101 = 3'b100
    } state_t;

    state_t current_state, next_state;

    always @(posedge clk) begin
        if (reset) begin
            current_state <= STATE_IDLE;
            start_shifting <= 0;
        end else begin
            current_state <= next_state;
            if (current_state == STATE_1101) begin
                start_shifting <= 1;
            end
        end
    end

    always @(*) begin
        case (current_state)
            STATE_IDLE: next_state = (data == 1'b1) ? STATE_1 : STATE_IDLE;
            STATE_1:    next_state = (data == 1'b1) ? STATE_11 : STATE_IDLE;
            STATE_11:   next_state = (data == 1'b0) ? STATE_110 : STATE_1;
            STATE_110:  next_state = (data == 1'b1) ? STATE_1101 : STATE_IDLE;
            STATE_1101: next_state = STATE_1101;
            default:    next_state = STATE_IDLE;
        endcase
    end

endmodule
