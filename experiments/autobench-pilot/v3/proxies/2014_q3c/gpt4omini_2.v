module top_module (
	input clk,
	input x,
	input [2:0] y,
	output reg Y0,
	output reg z
);
	reg [2:0] next_state;

	always @(posedge clk) begin
		y <= next_state;
	end
	
	always @(*) begin
		case (y)
			3'b000: next_state = (x) ? 3'b001 : 3'b000;
			3'b001: next_state = (x) ? 3'b100 : 3'b001;
			3'b010: next_state = (x) ? 3'b001 : 3'b010;
			3'b011: next_state = (x) ? 3'b010 : 3'b001;
			3'b100: next_state = (x) ? 3'b100 : 3'b011;
			default: next_state = 3'b000;
		endcase
	end
	
	always @(*) begin
		case (y)
			3'b000: z = 0;
			3'b001: z = 0;
			3'b010: z = 0;
			3'b011: z = 1;
			3'b100: z = 1;
			default: z = 0;
		endcase
	end
	
	always @(*) begin
		Y0 = y[0];
	end
endmodule
