module custom_byte_enable_ram #(
    parameter XLEN = 32,
    parameter LINES = 8192
) (
    input  logic                      clk,
    input  logic [$clog2(LINES)-1:0]  addr_a,
    input  logic                      en_a,
    input  logic [XLEN/8-1:0]         be_a,
    input  logic [XLEN-1:0]           data_in_a,
    output logic [XLEN-1:0]           data_out_a,
    input  logic [$clog2(LINES)-1:0]  addr_b,
    input  logic                      en_b,
    input  logic [XLEN/8-1:0]         be_b,
    input  logic [XLEN-1:0]           data_in_b,
    output logic [XLEN-1:0]           data_out_b
);

    localparam ADDR_WIDTH = $clog2(LINES);
    localparam BYTES = XLEN/8;

    logic [XLEN-1:0] ram [LINES-1:0];

    logic [ADDR_WIDTH-1:0] addr_a_reg, addr_b_reg;
    logic                  en_a_reg,   en_b_reg;
    logic [BYTES-1:0]      be_a_reg,   be_b_reg;
    logic [XLEN-1:0]       data_in_a_reg, data_in_b_reg;

    integer i;
    initial begin
        for (i = 0; i < LINES; i = i + 1)
            ram[i] = {XLEN{1'b0}};
    end

    always_ff @(posedge clk) begin
        addr_a_reg    <= addr_a;
        en_a_reg      <= en_a;
        be_a_reg      <= be_a;
        data_in_a_reg <= data_in_a;

        addr_b_reg    <= addr_b;
        en_b_reg      <= en_b;
        be_b_reg      <= be_b;
        data_in_b_reg <= data_in_b;
    end

    always_ff @(posedge clk) begin
        if (en_a_reg && en_b_reg && (addr_a_reg == addr_b_reg)) begin
            for (i = 0; i < BYTES; i = i + 1) begin
                if (be_a_reg[i])
                    ram[addr_a_reg][i*8 +: 8] <= data_in_a_reg[i*8 +: 8];
                else if (be_b_reg[i])
                    ram[addr_a_reg][i*8 +: 8] <= data_in_b_reg[i*8 +: 8];
            end
        end else begin
            if (en_a_reg) begin
                for (i = 0; i < BYTES; i = i + 1)
                    if (be_a_reg[i])
                        ram[addr_a_reg][i*8 +: 8] <= data_in_a_reg[i*8 +: 8];
            end
            if (en_b_reg) begin
                for (i = 0; i < BYTES; i = i + 1)
                    if (be_b_reg[i])
                        ram[addr_b_reg][i*8 +: 8] <= data_in_b_reg[i*8 +: 8];
            end
        end
    end

    always_ff @(posedge clk) begin
        data_out_a <= ram[addr_a_reg];
        data_out_b <= ram[addr_b_reg];
    end

endmodule
