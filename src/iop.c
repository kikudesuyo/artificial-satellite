void send_data_IO_preamble() {
 int1 calc_bit = downlink_data[0];
  
 int1 flag = 1;
 unsigned int8 bit;
 unsigned int16 timeout;
  
 for (unsigned int16 i = 0; i < downlink_data_size; i++) {
  for (timeout = 0, bit = 0; (bit < 8) && (timeout < 1000); timeout++) {
   if (!input(DOWNLINK_CLK_PIN) && flag) {
    output_bit(DOWNLINK_DATA_PIN, calc_bit);
    flag = 0;
    timeout = 0;
    bit++;
   }
   else if (input(DOWNLINK_CLK_PIN)) {
    flag = 1;
   }
  }
  if (timeout == 1000) {
   disp("downlink clock timeout\r\n");
  }
 } 
}