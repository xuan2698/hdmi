module signedadder #(
    parameter DATA_WIDTH = 8
) (
    input  wire                      i_clk,
    input  wire                      i_rst_n,
    input  wire                      i_enable,
    input  wire                      i_start,
    input  wire                      i_mode,
    input  wire                      i_clear,
    input  wire signed [DATA_WIDTH-1:0] i_operand_a,
    input  wire signed [DATA_WIDTH-1:0] i_operand_b,
    output reg  signed [DATA_WIDTH-1:0] o_resultant_sum,
    output reg                       o_overflow,
    output reg                       o_ready,
    output reg  [1:0]                o_status
);

    localparam [1:0] IDLE    = 2'b00;
    localparam [1:0] LOAD    = 2'b01;
    localparam [1:0] COMPUTE = 2'b10;
    localparam [1:0] OUTPUT  = 2'b11;

    reg [1:0] state;
    reg signed [DATA_WIDTH-1:0] reg_a;
    reg signed [DATA_WIDTH-1:0] reg_b;
    reg mode_reg;

    wire signed [DATA_WIDTH:0] ext_a = {reg_a[DATA_WIDTH-1], reg_a};
    wire signed [DATA_WIDTH:0] ext_b = {reg_b[DATA_WIDTH-1], reg_b};
    wire signed [DATA_WIDTH:0] ext_sum = mode_reg ? (ext_a - ext_b) : (ext_a + ext_b);
    wire signed [DATA_WIDTH-1:0] sum_trunc = ext_sum[DATA_WIDTH-1:0];
    wire overflow_calc = (ext_sum[DATA_WIDTH] != ext_sum[DATA_WIDTH-1]);

    always @(posedge i_clk or negedge i_rst_n) begin
        if (!i_rst_n) begin
            state            <= IDLE;
            reg_a            <= {DATA_WIDTH{1'b0}};
            reg_b            <= {DATA_WIDTH{1'b0}};
            mode_reg         <= 1'b0;
            o_resultant_sum  <= {DATA_WIDTH{1'b0}};
            o_overflow       <= 1'b0;
            o_ready          <= 1'b0;
            o_status         <= IDLE;
        end else if (i_clear) begin
            state            <= IDLE;
            reg_a            <= {DATA_WIDTH{1'b0}};
            reg_b            <= {DATA_WIDTH{1'b0}};
            mode_reg         <= 1'b0;
            o_resultant_sum  <= {DATA_WIDTH{1'b0}};
            o_overflow       <= 1'b0;
            o_ready          <= 1'b0;
            o_status         <= IDLE;
        end else begin
            case (state)
                IDLE: begin
                    o_ready  <= 1'b0;
                    o_status <= IDLE;
                    if (i_enable && i_start) begin
                        state <= LOAD;
                    end
                end
                LOAD: begin
                    reg_a    <= i_operand_a;
                    reg_b    <= i_operand_b;
                    mode_reg <= i_mode;
                    o_status <= LOAD;
                    state    <= COMPUTE;
                end
                COMPUTE: begin
                    o_status <= COMPUTE;
                    state    <= OUTPUT;
                end
                OUTPUT: begin
                    o_resultant_sum <= sum_trunc;
                    o_overflow      <= overflow_calc;
                    o_ready         <= 1'b1;
                    o_status        <= OUTPUT;
                    state           <= IDLE;
                end
                default: begin
                    state    <= IDLE;
                    o_status <= IDLE;
                end
            endcase
        end
    end

endmodule
