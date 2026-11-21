module dig_stopwatch_tb;

  parameter CLK_FREQ = 200;
  localparam PERIOD = (1_000_000_000 / CLK_FREQ);

  reg clk;
  reg reset;
  reg start_stop;

  wire [5:0] seconds;
  wire [5:0] minutes;
  wire hour;

  dig_stopwatch #(.CLK_FREQ(CLK_FREQ)) uut (
    .clk(clk),
    .reset(reset),
    .start_stop(start_stop),
    .seconds(seconds),
    .minutes(minutes),
    .hour(hour)
  );

  initial clk = 1'b0;
  always #(PERIOD/2) clk = ~clk;

  initial begin
    $dumpfile("dig_stopwatch_tb.vcd");
    $dumpvars(0, dig_stopwatch_tb);

    reset = 1'b1;
    start_stop = 1'b0;
    #100;
    reset = 1'b0;

    start_stop = 1'b1;
    repeat (1000) @(posedge uut.one_sec_pulse);

    start_stop = 1'b0;
    repeat (200) @(posedge clk);

    start_stop = 1'b1;
    repeat (3000) @(posedge uut.one_sec_pulse);

    start_stop = 1'b0;
    repeat (500) @(posedge clk);

    reset = 1'b1;
    repeat (5) @(posedge clk);
    reset = 1'b0;

    start_stop = 1'b1;
    repeat (100) @(posedge uut.one_sec_pulse);

    start_stop = 1'b0;
    repeat (10) @(posedge clk);
    $finish;
  end

endmodule
