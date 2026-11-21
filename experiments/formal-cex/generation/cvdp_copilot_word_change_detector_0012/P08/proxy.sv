module Word_Change_Pulse #(
    parameter DATA_WIDTH = 8
) (
    input  logic                  clk,
    input  logic                  reset,
    input  logic [DATA_WIDTH-1:0] data_in,
    input  logic [DATA_WIDTH-1:0] mask,
    input  logic [DATA_WIDTH-1:0] match_pattern,
    input  logic                  enable,
    input  logic                  latch_pattern,
    output logic                  word_change_pulse,
    output logic                  pattern_match_pulse,
    output logic [DATA_WIDTH-1:0] latched_pattern
);

    logic [DATA_WIDTH-1:0] data_in_prev;
    logic [DATA_WIDTH-1:0] masked_change;
    logic [DATA_WIDTH-1:0] masked_data;
    logic [DATA_WIDTH-1:0] masked_latched;

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            data_in_prev      <= '0;
            latched_pattern   <= '0;
            word_change_pulse <= 1'b0;
            pattern_match_pulse <= 1'b0;
        end else begin
            data_in_prev <= data_in;

            if (latch_pattern)
                latched_pattern <= match_pattern;

            if (enable) begin
                masked_change = (data_in ^ data_in_prev) & mask;
                word_change_pulse <= (masked_change != '0);

                masked_data    = data_in & mask;
                masked_latched = latched_pattern & mask;
                pattern_match_pulse <= (masked_data == masked_latched);
            end else begin
                word_change_pulse   <= 1'b0;
                pattern_match_pulse <= 1'b0;
            end
        end
    end

endmodule
