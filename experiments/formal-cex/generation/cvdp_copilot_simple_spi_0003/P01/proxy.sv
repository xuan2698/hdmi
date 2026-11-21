module spi_fsm (
    input  logic        i_clk,
    input  logic        i_rst_b,
    input  logic [15:0] i_data_in,
    input  logic        i_enable,
    input  logic        i_fault,
    input  logic        i_clear,
    output logic        o_spi_cs_b,
    output logic        o_spi_clk,
    output logic        o_spi_data,
    output logic [4:0]  o_bits_left,
    output logic        o_done,
    output logic [1:0]  o_fsm_state
);

    localparam logic [1:0] IDLE  = 2'b00;
    localparam logic [1:0] TX    = 2'b01;
    localparam logic [1:0] TOGGLE= 2'b10;
    localparam logic [1:0] ERROR = 2'b11;

    logic [1:0]  state, next_state;
    logic [15:0] shift_reg;
    logic [4:0]  bits_left;
    logic        spi_clk_r;
    logic        spi_data_r;
    logic        spi_cs_b_r;
    logic        done_r;

    assign o_fsm_state = state;
    assign o_spi_cs_b  = spi_cs_b_r;
    assign o_spi_clk   = spi_clk_r;
    assign o_spi_data  = spi_data_r;
    assign o_bits_left = bits_left;
    assign o_done      = done_r;

    always_ff @(posedge i_clk or negedge i_rst_b) begin
        if (!i_rst_b) begin
            state       <= IDLE;
            shift_reg   <= 16'h0000;
            bits_left   <= 5'd16;
            spi_clk_r   <= 1'b0;
            spi_data_r  <= 1'b0;
            spi_cs_b_r  <= 1'b1;
            done_r      <= 1'b0;
        end else begin
            done_r <= 1'b0;

            if (i_clear) begin
                state       <= IDLE;
                shift_reg   <= 16'h0000;
                bits_left   <= 5'd16;
                spi_clk_r   <= 1'b0;
                spi_data_r  <= 1'b0;
                spi_cs_b_r  <= 1'b1;
            end else if (i_fault) begin
                state       <= ERROR;
                bits_left   <= 5'd16;
                spi_clk_r   <= 1'b0;
                spi_data_r  <= 1'b0;
                spi_cs_b_r  <= 1'b1;
                done_r      <= 1'b1;
            end else if (!i_enable) begin
                state       <= IDLE;
                shift_reg   <= 16'h0000;
                bits_left   <= 5'd16;
                spi_clk_r   <= 1'b0;
                spi_data_r  <= 1'b0;
                spi_cs_b_r  <= 1'b1;
            end else begin
                case (state)
                    IDLE: begin
                        spi_cs_b_r <= 1'b1;
                        spi_clk_r  <= 1'b0;
                        spi_data_r <= 1'b0;
                        bits_left  <= 5'd16;
                        if (i_enable) begin
                            shift_reg  <= i_data_in;
                            spi_cs_b_r <= 1'b0;
                            spi_data_r <= i_data_in[15];
                            state      <= TX;
                        end
                    end

                    TX: begin
                        spi_cs_b_r <= 1'b0;
                        spi_clk_r  <= 1'b1;
                        state      <= TOGGLE;
                    end

                    TOGGLE: begin
                        spi_clk_r <= 1'b0;
                        if (bits_left > 5'd1) begin
                            shift_reg  <= {shift_reg[14:0], 1'b0};
                            spi_data_r <= shift_reg[14];
                            bits_left  <= bits_left - 5'd1;
                            state      <= TX;
                        end else begin
                            bits_left  <= 5'd16;
                            spi_data_r <= 1'b0;
                            spi_cs_b_r <= 1'b1;
                            done_r     <= 1'b1;
                            state      <= IDLE;
                        end
                    end

                    ERROR: begin
                        spi_cs_b_r <= 1'b1;
                        spi_clk_r  <= 1'b0;
                        spi_data_r <= 1'b0;
                        bits_left  <= 5'd16;
                        done_r     <= 1'b0;
                        state      <= ERROR;
                    end

                    default: state <= IDLE;
                endcase
            end
        end
    end

endmodule
