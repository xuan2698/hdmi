module top_module (
    input clk,
    input a,
    input b,
    output reg q,
    output reg state
);

    always @(posedge clk) begin
        state <= q; // the state output follows the current q
        
        // Determine the next state of q based on current inputs a and b
        if (a & b)
            q <= ~q; // toggle q when both a and b are 1
        else if (a)
            q <= 1; // set q to 1 when only a is 1
        else
            q <= 0; // set q to 0 for all other conditions
    end

endmodule
