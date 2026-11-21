module spi_fsm (
    input  wire        i_clk,
    input  wire        i_rst_b,
    input  wire [15:0] i_data_in,
    input  wire        i_enable,
    input  wire        i_fault,
    input  wire        i_clear,
    output reg         o_spi_cs_b,
    output reg         o_spi_clk,
    output reg         o_spi_data,
    output reg  [4:0]  o_bits_left,
    output reg         o_done,
    output reg  [1:0]  o_fsm_state
);

    localparam [1:0] IDLE  = 2'b00;
    localparam [1:0] TX    = 2'b01;
    localparam [1:0] TOGGLE= 2'b10;
    localparam [1:0] ERROR = 2'b11;

    reg [15:0] shift_reg;
    reg [4:0]  bit_cnt;
    reg        clk_phase;

    always @(posedge i_clk or negedge i_rst_b) begin
        if (!i_rst_b) begin
            o_spi_cs_b   <= 1'b1;
            o_spi_clk    <= 1'b0;
            o_spi_data   <= 1'b0;
            o_bits_left  <= 5'd16;
            o_done       <= 1'b0;
            o_fsm_state  <= IDLE;
            shift_reg    <= 16'd0;
            bit_cnt      <= 5'd0;
            clk_phase    <= 1'b0;
        end else begin
            o_done <= 1'b0;

            if (i_clear) begin
                o_spi_cs_b  <= 1'b1;
                o_spi_clk   <= 1'b0;
                o_spi_data  <= 1'b0;
                o_bits_left <= 5'd16;
                o_fsm_state <= IDLE;
                shift_reg   <= 16'd0;
                bit_cnt     <= 5'd0;
                clk_phase   <= 1'b0;
            end else if (i_fault) begin
                o_spi_cs_b  <= 1'b1;
                o_spi_clk   <= 1'b0;
                o_spi_data  <= 1'b0;
                o_bits_left <= 5'd16;
                o_done      <= 1'b1;
                o_fsm_state <= ERROR;
                shift_reg   <= 16'd0;
                bit_cnt     <= 5'd0;
                clk_phase   <= 1'b0;
            end else if (!i_enable) begin
                o_spi_cs_b  <= 1'b1;
                o_spi_clk   <= 1'b0;
                o_spi_data  <= 1'b0;
                o_bits_left <= 5'd16;
                o_fsm_state <= IDLE;
                shift_reg   <= 16'd0;
                bit_cnt     <= 5'd0;
                clk_phase   <= 1'b0;
            end else begin
                case (o_fsm_state)
                    IDLE: begin
                        o_spi_cs_b  <= 1'b1;
                        o_spi_clk   <= 1'b0;
                        o_spi_data  <= 1'b0;
                        o_bits_left <= 5'd16;
                        shift_reg   <= i_data_in;
                        bit_cnt     <= 5'd0;
                        clk_phase   <= 1'b0;
                        o_fsm_state <= TX;
                    end

                    TX: begin
                        o_spi_cs_b  <= 1'b0;
                        o_spi_clk   <= 1'b0;
                        o_spi_data  <= shift_reg[15];
                        o_bits_left <= 5'd16 - bit_cnt;
                        clk_phase   <= 1'b0;
                        o_fsm_state <= TOGGLE;
                    end

                    TOGGLE: begin
                        if (!clk_phase) begin
                            o_spi_clk  <= 1'b1;
                            clk_phase  <= 1'b1;
                        end else begin
                            o_spi_clk  <= 1'b0;
                            clk_phase  <= 1'b0;
                            shift_reg  <= {shift_reg[14:0], 1'b0};
                            bit_cnt    <= bit_cnt + 5'd1;
                            if (bit_cnt == 5'd15) begin
                                o_bits_left <= 5'd0;
                                o_done      <= 1'b1;
                                o_spi_cs_b  <= 1'b1;
                                o_spi_data  <= 1'b0;
                                o_fsm_state <= IDLE;
                            end else begin
                                o_bits_left <= 5'd15 - bit_cnt;
                                o_fsm_state <= TX;
                            end
                        end
                    end

                    ERROR: begin
                        o_spi_cs_b  <= 1'b1;
                        o_spi_clk   <= 1'b0;
                        o_spi_data  <= 1'b0;
                        o_bits_left <= 5'd16;
                        o_fsm_state <= ERROR;
                    end

                    default: o_fsm_state <= IDLE;
                endcase
            end
        end
    end

endmodule
