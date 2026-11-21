module hill_cipher (
    input  wire        clk,
    input  wire        reset,
    input  wire        start,
    input  wire [14:0] plaintext,
    input  wire [44:0] key,
    output reg  [14:0] ciphertext,
    output reg         done
);

    localparam IDLE        = 2'd0;
    localparam COMPUTE     = 2'd1;
    localparam COMPUTE_MOD = 2'd2;
    localparam DONE        = 2'd3;

    reg [1:0] state;

    reg [14:0] pt_reg;
    reg [44:0] key_reg;

    reg [9:0]  sum0;
    reg [9:0]  sum1;
    reg [9:0]  sum2;

    wire [4:0] p0 = pt_reg[4:0];
    wire [4:0] p1 = pt_reg[9:5];
    wire [4:0] p2 = pt_reg[14:10];

    wire [4:0] k00 = key_reg[4:0];
    wire [4:0] k01 = key_reg[9:5];
    wire [4:0] k02 = key_reg[14:10];
    wire [4:0] k10 = key_reg[19:15];
    wire [4:0] k11 = key_reg[24:20];
    wire [4:0] k12 = key_reg[29:25];
    wire [4:0] k20 = key_reg[34:30];
    wire [4:0] k21 = key_reg[39:35];
    wire [4:0] k22 = key_reg[44:40];

    wire [9:0] prod00 = p0 * k00;
    wire [9:0] prod01 = p1 * k01;
    wire [9:0] prod02 = p2 * k02;
    wire [9:0] prod10 = p0 * k10;
    wire [9:0] prod11 = p1 * k11;
    wire [9:0] prod12 = p2 * k12;
    wire [9:0] prod20 = p0 * k20;
    wire [9:0] prod21 = p1 * k21;
    wire [9:0] prod22 = p2 * k22;

    wire [9:0] sum0_c = prod00 + prod01 + prod02;
    wire [9:0] sum1_c = prod10 + prod11 + prod12;
    wire [9:0] sum2_c = prod20 + prod21 + prod22;

    function [4:0] mod26;
        input [9:0] val;
        reg [9:0] tmp;
        begin
            tmp = val;
            while (tmp >= 10'd26)
                tmp = tmp - 10'd26;
            mod26 = tmp[4:0];
        end
    endfunction

    wire [4:0] c0 = mod26(sum0);
    wire [4:0] c1 = mod26(sum1);
    wire [4:0] c2 = mod26(sum2);

    always @(posedge clk) begin
        if (reset) begin
            state      <= IDLE;
            pt_reg     <= 15'd0;
            key_reg    <= 45'd0;
            sum0       <= 10'd0;
            sum1       <= 10'd0;
            sum2       <= 10'd0;
            ciphertext <= 15'd0;
            done       <= 1'b0;
        end else begin
            case (state)
                IDLE: begin
                    done <= 1'b0;
                    if (start) begin
                        pt_reg  <= plaintext;
                        key_reg <= key;
                        state   <= COMPUTE;
                    end
                end
                COMPUTE: begin
                    sum0  <= sum0_c;
                    sum1  <= sum1_c;
                    sum2  <= sum2_c;
                    state <= COMPUTE_MOD;
                end
                COMPUTE_MOD: begin
                    ciphertext <= {c2, c1, c0};
                    state      <= DONE;
                end
                DONE: begin
                    done  <= 1'b1;
                    state <= IDLE;
                end
                default: state <= IDLE;
            endcase
        end
    end

endmodule
