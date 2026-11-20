module top_module (
    input clk,
    input in,
    input reset,
    output out
);
    parameter A=0, B=1, C=2, D=3;
    reg [1:0] state;
    reg [1:0] next;
    
    always_comb begin
        case (state)
            A: next = in ? B : A; // No change
            // Mutation: Change next state for B when in=0 from C to D
            B: next = in ? B : D; // Changed here
            C: next = in ? D : A; // No change
            D: next = in ? B : C; // No change
        endcase
    end
    
    always @(posedge clk) begin
        if (reset) state <= A;
        else state <= next;
    end
        
    assign out = (state==D);

endmodule
