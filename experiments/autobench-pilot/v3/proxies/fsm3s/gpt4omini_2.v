module top_module (
	input clk,
	input in,
	input reset,
	output reg out
);

typedef enum reg [1:0] {A, B, C, D} state_t;
state_t state, next_state;

always @(posedge clk or posedge reset) begin
	if (reset) begin
		state <= A;
	end else begin
		state <= next_state;
	end
end

always @(*) begin
	case (state)
		A: begin
			next_state = (in == 0) ? A : B;
			out = 0;
		end
		B: begin
			next_state = (in == 0) ? C : B;
			out = 0;
		end
		C: begin
			next_state = (in == 0) ? A : D;
			out = 0;
		end
		D: begin
			next_state = (in == 0) ? C : B;
			out = 1;
		end
		default: begin
			next_state = A;
			out = 0;
		end
	endcase
end

endmodule
