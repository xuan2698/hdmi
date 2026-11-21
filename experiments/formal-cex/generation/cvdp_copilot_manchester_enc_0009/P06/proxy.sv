module top_manchester #(
    parameter N = 8
) (
    input  logic           clk_in,
    input  logic           rst_in,
    input  logic           enc_valid_in,
    input  logic [N-1:0]   enc_data_in,
    input  logic           dec_valid_in,
    input  logic [2*N-1:0] dec_data_in,
    output logic           enc_valid_out,
    output logic [2*N-1:0] enc_data_out,
    output logic           dec_valid_out,
    output logic [N-1:0]   dec_data_out
);

    always_ff @(posedge clk_in or posedge rst_in) begin
        if (rst_in) begin
            enc_valid_out <= 1'b0;
            enc_data_out  <= '0;
            dec_valid_out <= 1'b0;
            dec_data_out  <= '0;
        end else begin
            enc_valid_out <= enc_valid_in;
            if (enc_valid_in) begin
                for (int i = 0; i < N; i++) begin
                    enc_data_out[2*i]   <= ~enc_data_in[i];
                    enc_data_out[2*i+1] <=  enc_data_in[i];
                end
            end

            dec_valid_out <= dec_valid_in;
            if (dec_valid_in) begin
                for (int i = 0; i < N; i++) begin
                    if (dec_data_in[2*i] == 1'b0 && dec_data_in[2*i+1] == 1'b1)
                        dec_data_out[i] <= 1'b1;
                    else
                        dec_data_out[i] <= 1'b0;
                end
            end
        end
    end

endmodule
