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

    reg [12:0] sum0;
    reg [12:0] sum1;
    reg [12:0] sum2;

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

    wire [9:0] m00 = p0 * k00;
    wire [9:0] m01 = p1 * k01;
    wire [9:0] m02 = p2 * k02;
    wire [9:0] m10 = p0 * k10;
    wire [9:0] m11 = p1 * k11;
    wire [9:0] m12 = p2 * k12;
    wire [9:0] m20 = p0 * k20;
    wire [9:0] m21 = p1 * k21;
    wire [9:0] m22 = p2 * k22;

    wire [11:0] s0 = m00 + m01 + m02;
    wire [11:0] s1 = m10 + m11 + m12;
    wire [11:0] s2 = m20 + m21 + m22;

    function [4:0] mod26;
        input [12:0] val;
        reg [12:0] v;
        begin
            v = val;
            while (v >= 13'd26)
                v = v - 13'd26;
            mod26 = v[4:0];
        end
    endfunction

    always @(posedge clk) begin
        if (reset) begin
            state      <= IDLE;
            ciphertext <= 15'd0;
            done       <= 1'b0;
            pt_reg     <= 15'd0;
            key_reg    <= 45'd0;
            sum0       <= 13'd0;
            sum1       <= 13'd0;
            sum2       <= 13'd0;
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
                    sum0  <= {1'b0, s0};
                    sum1  <= {1'b0, s1};
                    sum2  <= {1'b0, s2};
                    state <= COMPUTE_MOD;
                end
                COMPUTE_MOD: begin
                    ciphertext <= {mod26(sum2), mod26(sum1), mod26(sum0)};
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
