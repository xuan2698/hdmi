module top_module(
    input clk,
    input reset,
    input data,
    output reg start_shifting);

    reg [2:0] state;
    
    parameter S0 = 3'b000, 
              S1 = 3'b001, 
              S2 = 3'b010, 
              S3 = 3'b011;

    always @(posedge clk) begin
        if (reset) begin
            state <= S0;
            start_shifting <= 0;
        end else begin
            case (state)
                S0: if (data) state <= S1; // 1
                    else state <= S0;
                S1: if (data) state <= S2; // 11
                    else state <= S0;
                S2: if (!data) state <= S3; // 110
                    else state <= S2;
                S3: if (data) begin
                        start_shifting <= 1; // 1101 found
                        state <= S0; // Reset for new search
                    end else 
                        state <= S0;
            endcase
        end
    end
endmodule
