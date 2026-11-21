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

    reg [4:0] p0, p1, p2;
    reg [4:0] k00, k01, k02;
    reg [4:0] k10, k11, k12;
    reg [4:0] k20, k21, k22;

    reg [11:0] sum0, sum1, sum2;

    wire [11:0] prod00 = p0 * k00;
    wire [11:0] prod01 = p1 * k01;
    wire [11:0] prod02 = p2 * k02;
    wire [11:0] prod10 = p0 * k10;
    wire [11:0] prod11 = p1 * k11;
    wire [11:0] prod12 = p2 * k12;
    wire [11:0] prod20 = p0 * k20;
    wire [11:0] prod21 = p1 * k21;
    wire [11:0] prod22 = p2 * k22;

    function [4:0] mod26;
        input [11:0] val;
        reg [11:0] tmp;
        begin
            tmp = val;
            while (tmp >= 12'd26)
                tmp = tmp - 12'd26;
            mod26 = tmp[4:0];
        end
    endfunction

    always @(posedge clk) begin
        if (reset) begin
            state      <= IDLE;
            ciphertext <= 15'd0;
            done       <= 1'b0;
            p0 <= 5'd0; p1 <= 5'd0; p2 <= 5'd0;
            k00 <= 5'd0; k01 <= 5'd0; k02 <= 5'd0;
            k10 <= 5'd0; k11 <= 5'd0; k12 <= 5'd0;
            k20 <= 5'd0; k21 <= 5'd0; k22 <= 5'd0;
            sum0 <= 12'd0; sum1 <= 12'd0; sum2 <= 12'd0;
        end else begin
            case (state)
                IDLE: begin
                    done <= 1'b0;
                    if (start) begin
                        p0  <= plaintext[4:0];
                        p1  <= plaintext[9:5];
                        p2  <= plaintext[14:10];
                        k00 <= key[4:0];
                        k01 <= key[9:5];
                        k02 <= key[14:10];
                        k10 <= key[19:15];
                        k11 <= key[24:20];
                        k12 <= key[29:25];
                        k20 <= key[34:30];
                        k21 <= key[39:35];
                        k22 <= key[44:40];
                        state <= COMPUTE;
                    end
                end
                COMPUTE: begin
                    sum0 <= prod00 + prod01 + prod02;
                    sum1 <= prod10 + prod11 + prod12;
                    sum2 <= prod20 + prod21 + prod22;
                    state <= COMPUTE_MOD;
                end
                COMPUTE_MOD: begin
                    ciphertext <= {mod26(sum2), mod26(sum1), mod26(sum0)};
                    state <= DONE;
                end
                DONE: begin
                    done <= 1'b1;
                    state <= IDLE;
                end
                default: state <= IDLE;
            endcase
        end
    end

endmodule
