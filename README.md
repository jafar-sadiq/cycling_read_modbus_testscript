# cycling_read_modbus_testscript
1.Check read data for each registers that added in the psu-testing script2.bash.	

2. There are two types of modbus registers, one is fix value register (Ex. 0x10, 0x30, x038, 0x40), the other is variable value register (Ex. 0x8c, 0x8a, 0x96). 
	For fix value registers --- Compare the read rata with the first time read data, stop the test if the data does not match with the first time read data. 
	For variable value registers -- Check the read data whether within the setting range.(Minimum > read data > Maximum), stop the test if the data out of the setting range. The default setting range as following.
	0x8a --> 12 < read data < 13
	0x8c --> 10 < read data <265
	0x96 --> 30 < read data < 3300
	
3. Allow to modify the test script for adding new registers or changing checking range parameters based on the applications.
