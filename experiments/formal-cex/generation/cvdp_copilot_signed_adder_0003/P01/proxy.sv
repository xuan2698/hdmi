module signedadder #(
    parameter DATA_WIDTH = 8
) (
    input  wire                          i_clk,
    input  wire                          i_rst_n,
    input  wire                          i_start,
    input  wire                          i_enable,
    input  wire                          i_mode,
    input  wire                          i_clear,
    input  wire signed [DATA_WIDTH-1:0]  i_operand_a,
    input  wire signed [DATA_WIDTH-1:0]  i_operand_b,
    output reg  signed [DATA_WIDTH-1:0]  o_resultant_sum,
    output reg                           o_overflow,
    output reg                           o_ready,
    output reg  [1:0]                    o_status
);

    localparam [1:0] IDLE    = 2'b00;
    localparam [1:0] LOAD    = 2'b01;
    localparam [1:0] COMPUTE = 2'b10;
    localparam [1:0] OUTPUT  = 2'b11;

    reg [1:0] state, next_state;
    reg signed [DATA_WIDTH-1:0] operand_a_reg, operand_b_reg;
    reg mode_reg;
    reg signed [DATA_WIDTH-1:0] sum_comb;
    reg overflow_comb;

    always @(*) begin
        case (state)
            IDLE:    next_state = (i_enable && i_start) ? LOAD : IDLE;
            LOAD:    next_state = COMPUTE;
            COMPUTE: next_state = OUTPUT;
            OUTPUT:  next_state = IDLE;
            default: next_state = IDLE;
        endcase
    end

    always @(posedge i_clk or negedge i_rst_n) begin
        if (!i_rst_n) begin
            state          <= IDLE;
            operand_a_reg  <= {DATA_WIDTH{1'b0}};
            operand_b_reg  <= {DATA_WIDTH{1'b0}};
            mode_reg       <= 1'b0;
            o_resultant_sum<= {DATA_WIDTH{1'b0}};
            o_overflow     <= 1'b0;
            o_ready        <= 1'b0;
            o_status       <= IDLE;
        end else if (i_clear) begin
            state          <= IDLE;
            operand_a_reg  <= {DATA_WIDTH{1'b0}};
            operand_b_reg  <= {DATA_WIDTH{1'b0}};
            mode_reg       <= 1'b0;
            o_resultant_sum<= {DATA_WIDTH{1'b0}};
            o_overflow     <= 1'b0;
            o_ready        <= 1'b0;
            o_status       <= IDLE;
        end else begin
            state    <= next_state;
            o_status <= next_state;
            case (state)
                IDLE: begin
                    o_ready <= 1'b0;
                end
                LOAD: begin
                    operand_a_reg <= i_operand_a;
                    operand_b_reg <= i_operand_b;
                    mode_reg      <= i_mode;
                end
                COMPUTE: begin
                    if (mode_reg)
                        sum_comb = operand_a_reg - operand_b_reg;
                    else
                        sum_comb = operand_a_reg + operand_b_reg;

                    if (mode_reg) begin
                        if ((operand_a_reg[DATA_WIDTH-1] != operand_b_reg[DATA_WIDTH-1]) &&
                            (sum_comb[DATA_WIDTH-1] != operand_a_reg[DATA_WIDTH-1]))
                            overflow_comb = 1'b1;
                        else
                            overflow_comb = 1'b0;
                    end else begin
                        if ((operand_a_reg[DATA_WIDTH-1] == operand_b_reg[DATA_WIDTH-1]) &&
                            (sum_comb[DATA_WIDTH-1] != operand_a_reg[DATA_WIDTH-1]))
                            overflow_comb = 1'b1;
                        else
                            overflow_comb = 1'b0;
                    end
                end
                OUTPUT: begin
                    o_resultant_sum <= sum_comb;
                    o_overflow      <= overflow_comb;
                    o_ready         <= 1'b1;
                end
                default: begin
                    o_ready <= 1'b0;
                end
            endcase
        end
    end

endmodule
