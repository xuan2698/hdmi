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

    reg [14:0] sum_reg;
    reg [14:0] ct_reg;

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

    wire [14:0] prod0_0 = p0 * k00;
    wire [14:0] prod0_1 = p1 * k01;
    wire [14:0] prod0_2 = p2 * k02;
    wire [14:0] prod1_0 = p0 * k10;
    wire [14:0] prod1_1 = p1 * k11;
    wire [14:0] prod1_2 = p2 * k12;
    wire [14:0] prod2_0 = p0 * k20;
    wire [14:0] prod2_1 = p1 * k21;
    wire [14:0] prod2_2 = p2 * k22;

    wire [14:0] sum0 = prod0_0 + prod0_1 + prod0_2;
    wire [14:0] sum1 = prod1_0 + prod1_1 + prod1_2;
    wire [14:0] sum2 = prod2_0 + prod2_1 + prod2_2;

    function [4:0] mod26;
        input [14:0] val;
        reg [14:0] tmp;
        begin
            tmp = val;
            while (tmp >= 15'd26)
                tmp = tmp - 15'd26;
            mod26 = tmp[4:0];
        end
    endfunction

    wire [4:0] m0 = mod26(sum_reg[14:0]);
    wire [4:0] m1 = mod26(sum_reg[14:0] >> 5);
    wire [4:0] m2 = mod26(sum_reg[14:0] >> 10);

    always @(posedge clk) begin
        if (reset) begin
            state      <= IDLE;
            done       <= 1'b0;
            ciphertext <= 15'd0;
            pt_reg     <= 15'd0;
            key_reg    <= 45'd0;
            sum_reg    <= 15'd0;
            ct_reg     <= 15'd0;
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
                    sum_reg <= {sum2[4:0], sum1[4:0], sum0[4:0]};
                    state   <= COMPUTE_MOD;
                end
                COMPUTE_MOD: begin
                    ct_reg     <= {m2, m1, m0};
                    ciphertext <= {m2, m1, m0};
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
