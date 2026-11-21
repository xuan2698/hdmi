module top_module (
    input clk,
    input areset,
    input x,
    output reg z
);
    reg [3:0] state;
    reg [3:0] count;
    reg [15:0] data; // Assuming max 16-bit input
    reg done;

    parameter IDLE = 4'b0000,
              READ = 4'b0001,
              COMPLEMENT = 4'b0010,
              OUTPUT = 4'b0011;

    always @(posedge clk or posedge areset) begin
        if (areset) begin
            state <= IDLE;
            count <= 0;
            data <= 0;
            z <= 0;
            done <= 0;
        end else begin
            case (state)
                IDLE: begin
                    if (!areset) begin
                        state <= READ;
                        count <= 0;
                        done <= 0;
                    end
                end
                READ: begin
                    if (count < 16) begin
                        data[count] <= x; // Read input bit
                        count <= count + 1;
                    end else begin
                        state <= COMPLEMENT;
                    end
                end
                COMPLEMENT: begin
                    data <= ~data + 1; // 2's complement
                    state <= OUTPUT;
                end
                OUTPUT: begin
                    z <= data[count]; // Output the most significant bit first
                    if (count > 0) begin
                        count <= count - 1;
                    end else begin
                        done <= 1; // Indicate process is done
                        state <= IDLE;
                    end
                end
            endcase
        end
    end
endmodule
