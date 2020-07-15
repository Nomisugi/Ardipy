# Ardipy
I made a tool to connect Arduino and PC (Python) easily.
This tool provides a function that allows you to easily use Arudino's I2C, PORT, and AD.
USB (UART: Virtual Com Port) is used to connect the PC and Arduino.
I want to make this tool very simple, so if you want to use complicated functions, I recommend using Pymate.

I used to use Aardvark to convert I2C and USB.
But this tool is very expensive.　Also, it was not compatible with python ver3.

The program structure is as follows
1. Ardipy.ino                     : For Arudino UNO　 UART　Control 
2. Ardipy_driver.py               : For Python3  (Connect to Arduino UNO)
3. Ardipy_I2CRegister.py   Ardipy : Python3 Sample Soft( I2C Register Controler ) 
4. Ardipy_ADGraph.py       Ardipy : Python3 Sample Soft( ADC Graph viewer )  (only ADC1, ADC2)
5. Ardipy_PortControler.py Ardipy : Python3 Sample Soft( Port Controler )  [Preparing]
6. Ardipy_PWMEditor.py Ardipy     : Python3 Sample Soft( PWMEditor )  [Preparing]
7. Ardipy_I2Craph.py       Ardipy : Python3 Sample Soft( I2C Registor Graph viewer )  [Preparing]
8. Ardipy_E2PROMEditor.py Ardipy  : Python3 Sample Soft( EEPROM ditor )  [Preparing]
9. Ardipy_Sequencer.py Ardipy     : Python3 Sample Soft( Arduino Sequencer )  [TBD]

---GUI Parts--- <BR>
HexSpinbox (Tkinter Hex spinbox) <BR>
LogWindow  (Tkinter LogWindow) <BR>
<BR>

---Problem and Issue---<BR>
SPI, PWM  ...
I2CRegister : write Save/Load
I2CRegister : Device Change
