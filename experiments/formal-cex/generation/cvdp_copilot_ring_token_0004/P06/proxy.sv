module token_ring_fsm (
    input  logic       clk,
    input  logic       rst,
    input  logic [3:0] data_in,
    input  logic       has_data_to_send,
    output logic [3:0] data_out,
    output logic [3:0] token_received,
    output logic [3:0] token
);

    typedef enum logic [1:0] {
        NODE0 = 2'b00,
        NODE1 = 2'b01,
        NODE2 = 2'b10,
        NODE3 = 2'b11
    } state_t;

    state_t state, next_state;

    always_ff @(posedge clk or posedge rst) begin
        if (rst)
            state <= NODE0;
        else
            state <= next_state;
    end

    always_comb begin
        next_state = state;
        case (state)
            NODE0: next_state = NODE1;
            NODE1: next_state = NODE2;
            NODE2: next_state = NODE3;
            NODE3: next_state = NODE0;
            default: next_state = NODE0;
        endcase
    end

    always_comb begin
        case (state)
            NODE0: begin
                token_received = 4'b0001;
                token          = 4'b0010;
            end
            NODE1: begin
                token_received = 4'b0010;
                token          = 4'b0100;
            end
            NODE2: begin
                token_received = 4'b0100;
                token          = 4'b1000;
            end
            NODE3: begin
                token_received = 4'b1000;
                token          = 4'b0001;
            end
            default: begin
                token_received = 4'b0001;
                token          = 4'b0010;
            end
        endcase
    end

    always_comb begin
        if (has_data_to_send)
            data_out = data_in;
        else
            data_out = 4'b0000;
    end

endmodule
