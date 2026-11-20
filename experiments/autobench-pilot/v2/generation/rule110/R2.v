module top_module(
    input clk,
    input load,
    input [511:0] data,
    output reg [511:0] q);

    always @(posedge clk) begin
        if (load) begin
            q <= data;
        end else begin
            integer i;
            reg [511:0] q_next;
            for (i = 0; i < 512; i = i + 1) begin
                case ({(i > 0 ? q[i-1] : 1'b0), q[i], (i < 511 ? q[i+1] : 1'b0)})
                    3'b111: q_next[i] = 0;
                    3'b110: q_next[i] = 1;
                    3'b101: q_next[i] = 1;
                    3'b100: q_next[i] = 0;
                    3'b011: q_next[i] = 1;
                    3'b010: q_next[i] = 1;
                    3'b001: q_next[i] = 1;
                    3'b000: q_next[i] = 0;
                    default: q_next[i] = 0; // default is only for safety, should match above cases
                endcase
            end
            q <= q_next;
        end
    end

endmodule
