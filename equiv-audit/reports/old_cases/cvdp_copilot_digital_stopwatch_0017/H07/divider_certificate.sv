
module gold(input [26:0] counter, input one_sec_pulse, input reset, input start_stop,
              output reg [26:0] next_counter, output reg next_one_sec_pulse);
localparam COUNTER_MAX=49999999;
always @* begin
    next_counter=counter;
    next_one_sec_pulse=one_sec_pulse;
    
        if (reset) begin
            next_counter = 0;
            next_one_sec_pulse = 0;
        end else begin
            if (start_stop) begin
                if (counter == COUNTER_MAX) begin
                    next_counter = 0;
                    next_one_sec_pulse = 1'b1;        // Generate a pulse every second
                end else begin
                    next_counter = counter + 1;
                    next_one_sec_pulse = 1'b0;
                end
            end else begin
                next_one_sec_pulse = 1'b0;           // Ensure one_sec_pulse is cleared if paused
            end
        end
    
end
endmodule

module variant(input [26:0] counter, input one_sec_pulse, input reset, input start_stop,
              output reg [26:0] next_counter, output reg next_one_sec_pulse);
localparam COUNTER_MAX=49999999;
always @* begin
    next_counter=counter;
    next_one_sec_pulse=one_sec_pulse;
    
        if (reset) begin
            next_counter = 0;
            next_one_sec_pulse = 0;
        end else begin
            if (1'b1) begin
                if (counter == COUNTER_MAX) begin
                    next_counter = 0;
                    next_one_sec_pulse = 1'b1;        // Generate a pulse every second
                end else begin
                    next_counter = counter + 1;
                    next_one_sec_pulse = 1'b0;
                end
            end else begin
                next_one_sec_pulse = 1'b0;           // Ensure one_sec_pulse is cleared if paused
            end
        end
    
end
endmodule

module cert(input [26:0] counter,input one_sec_pulse,input reset,input start_stop);
wire [26:0] gc, mc;
wire gp, mp;
wire terminal = counter == 27'd49999999;
gold g(counter,one_sec_pulse,reset,start_stop,gc,gp);
variant m(counter,one_sec_pulse,reset,start_stop,mc,mp);
always @* assert ((reset ? (gc==0 && !gp) : (start_stop ? (gc == (terminal ? 27'd0 : counter + 27'd1) && gp == terminal) : (gc==counter && !gp))) && (reset ? (mc==0 && !mp) : (mc == (terminal ? 27'd0 : counter + 27'd1) && mp == terminal)));
endmodule
