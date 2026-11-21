module custom_byte_enable_ram #(
    parameter XLEN = 32,
    parameter LINES = 8192
) (
    input  wire                     clk,
    input  wire [$clog2(LINES)-1:0] addr_a,
    input  wire                     en_a,
    input  wire [XLEN/8-1:0]        be_a,
    input  wire [XLEN-1:0]          data_in_a,
    output reg  [XLEN-1:0]          data_out_a,
    input  wire [$clog2(LINES)-1:0] addr_b,
    input  wire                     en_b,
    input  wire [XLEN/8-1:0]        be_b,
    input  wire [XLEN-1:0]          data_in_b,
    output reg  [XLEN-1:0]          data_out_b
);

    localparam ADDR_WIDTH = $clog2(LINES);
    localparam BYTES = XLEN / 8;

    logic [XLEN-1:0] ram [LINES-1:0];

    reg [ADDR_WIDTH-1:0] addr_a_reg;
    reg                  en_a_reg;
    reg [BYTES-1:0]      be_a_reg;
    reg [XLEN-1:0]       data_in_a_reg;

    reg [ADDR_WIDTH-1:0] addr_b_reg;
    reg                  en_b_reg;
    reg [BYTES-1:0]      be_b_reg;
    reg [XLEN-1:0]       data_in_b_reg;

    integer i;
    initial begin
        for (i = 0; i < LINES; i = i + 1) begin
            ram[i] = {XLEN{1'b0}};
        end
    end

    always @(posedge clk) begin
        addr_a_reg    <= addr_a;
        en_a_reg      <= en_a;
        be_a_reg      <= be_a;
        data_in_a_reg <= data_in_a;

        addr_b_reg    <= addr_b;
        en_b_reg      <= en_b;
        be_b_reg      <= be_b;
        data_in_b_reg <= data_in_b;
    end

    integer j;
    always @(posedge clk) begin
        if (en_a_reg && en_b_reg && (addr_a_reg == addr_b_reg)) begin
            for (j = 0; j < BYTES; j = j + 1) begin
                if (be_a_reg[j]) begin
                    ram[addr_a_reg][j*8 +: 8] <= data_in_a_reg[j*8 +: 8];
                end else if (be_b_reg[j]) begin
                    ram[addr_a_reg][j*8 +: 8] <= data_in_b_reg[j*8 +: 8];
                end
            end
        end else begin
            if (en_a_reg) begin
                for (j = 0; j < BYTES; j = j + 1) begin
                    if (be_a_reg[j]) begin
                        ram[addr_a_reg][j*8 +: 8] <= data_in_a_reg[j*8 +: 8];
                    end
                end
            end
            if (en_b_reg) begin
                for (j = 0; j < BYTES; j = j + 1) begin
                    if (be_b_reg[j]) begin
                        ram[addr_b_reg][j*8 +: 8] <= data_in_b_reg[j*8 +: 8];
                    end
                end
            end
        end

        data_out_a <= ram[addr_a_reg];
        data_out_b <= ram[addr_b_reg];
    end

endmodule
