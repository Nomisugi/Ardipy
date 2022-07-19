#include <Wire.h>

#define DEBUG_FLAG false
//#define BAUDRATE 9600
#define BAUDRATE 921600

const char* Version = "1.1!!"; //5 charactor

void debug_print(char* data)
{
  if(DEBUG_FLAG){
    Serial.println(data);
  }
}

void setup() {
  // put your setup code here, to run once:
  Wire.begin();
  Serial.begin(BAUDRATE);
  debug_print("Program start(Debug mode)");
}

static void writeRegister_word(unsigned char addr, byte reg, word value)
{
  Wire.beginTransmission(addr);
  Wire.write(reg);
  Wire.write((value >> 8) & 0xFF);
  Wire.write(value & 0xFF);
  Wire.endTransmission();
}


static void writeRegister_byte(unsigned char addr, byte reg, word value)
{
  Wire.beginTransmission(addr);
  Wire.write(reg);
//  Wire.write((value >> 8) & 0xFF);
  Wire.write(value & 0xFF);
  Wire.endTransmission();
}

static word readRegister_word(unsigned char addr, byte reg)
{
  word res = 0x0000;
  Wire.beginTransmission(addr);
  Wire.write(reg);

  if(Wire.endTransmission() == 0) {
    if(Wire.requestFrom(addr, 2) >= 2) {
      res = Wire.read() * 256;
      res += Wire.read();
    }
  }
  
  return res;
}

static char readRegister_byte(unsigned char addr, byte reg)
{
  char res = 0x00;
  Wire.beginTransmission(addr);
  Wire.write(reg);

  if(Wire.endTransmission() == 0) {
    if(Wire.requestFrom(addr, 1) >= 1) {
      res = Wire.read();
      }
  }
  
  return res;
}

int input_count=0;

// Format:
// I2R(Read I2C):38(SlaveAddress(HEX)):01(Registor):0 (文字数 1:1byte 2:2byte)!(終端文字)
//     -> (1byte)5byte return
//     -> (2byte)5byte return
// I2W(Write I2C):38(SlaveAddress(HEX)):01(Registor):FF(data):0 (文字数 0:1byte 2:2byte)!(終端文字)
//     -> 5byte return
// POW(write port):00(port No):1or0(Port Data)!(終端文字)  
//     -> 5byte return
// POR(read port):00(port No)!(終端文字)                   
//     -> 5byte return
// ADR(Read AD Data):00(AD port No)!(終端文字)
//     -> 5byte return
// VER(version)!(終端文字)
//     -> 5byte return

void loop() {
  char *lexeme;
  char buff[30];
  char input[30];   // 文字列格納用
  char str[5][10];
  char rets[30];
  long voltage;
  int  i;

//  test();
  if (Serial.available()) {
    input[input_count] = Serial.read();
     // 文字数が30以上 or 末尾文字
    if (input_count > 30 || input[input_count] == '!') {
      // 末尾に終端文字の挿入
      input[input_count] = '\0';
      for(lexeme = strtok(input, ":"); lexeme; lexeme = strtok(NULL, ":")) {
        debug_print(lexeme);
        strcpy(str[i], lexeme);
        i=i+1;
      }
      input_count = 0;
      i=0;

      if(strcmp( str[0], "I2R")==0){
        debug_print("Read I2C");
        if( atoi(str[3]) == 1){
          unsigned char retb = readRegister_byte(atoi16(str[1]), atoi16(str[2]));
          sprintf( buff, "SlaveAddr=%x : Registor=%x", atoi16(str[1]), atoi16(str[2]) );
          debug_print(buff);
          sprintf(rets, "%02x!!!", retb); 
          Serial.print(rets);
        }else{
          unsigned long retw = (unsigned short)readRegister_word(atoi16(str[1]), atoi16(str[2]));                  
          sprintf( buff, "SlaveAddr=%x : Registor=%x", atoi16(str[1]), atoi16(str[2]) );
          debug_print(buff);
          sprintf(rets, "%04x!", retw); 
          Serial.print(rets);
        }
      }
      else if(strcmp( str[0], "I2W")==0){
        debug_print("Write I2C");       
        if( atoi(str[4]) == 1){
          writeRegister_byte(atoi16(str[1]), atoi16(str[2]), atoi16(str[3]));
          Serial.print("!!!!!");
          if(DEBUG_FLAG){
            unsigned char retb = readRegister_byte(atoi16(str[1]), atoi16(str[2]));
            sprintf(rets, "Check Read data =%x", retb); 
            Serial.print(rets);
          } 
        }else{
          writeRegister_word(atoi16(str[1]), atoi16(str[2]), atoi16(str[3]));            
          Serial.print("!");
          if(DEBUG_FLAG){
            unsigned long retw = (unsigned short)readRegister_word(atoi16(str[1]), atoi16(str[2]));
            sprintf(rets, "Check Read data =%x", retw); 
            Serial.print(rets);
          } 
        }
      }
      else if(strcmp( str[0], "PWM")==0){
         pinMode(atoi16(str[1]), OUTPUT);
         writeRegister_byte(atoi16(str[1]), atoi16(str[2]), atoi16(str[3]));
         digitalWrite(atoi16(str[1]), atoi16(str[2]));
         debug_print("port out");
         Serial.print("!!!!!");
      }

      else if(strcmp( str[0], "POW")==0){
         pinMode(atoi16(str[1]), OUTPUT);
         digitalWrite(atoi16(str[1]), atoi16(str[2]));
         debug_print("port out");
         Serial.print("!!!!!");
      }
      else if(strcmp( str[0], "POR")==0){
         pinMode(atoi16(str[1]), INPUT);
         unsigned char retb = digitalRead(atoi16(str[1]));
         sprintf(rets, "%01x!!!!", retb); 
         Serial.print(rets);
      }
      else if(strcmp( str[0], "ADR")==0){
         word retw = analogRead(atoi16(str[1]));
         sprintf(rets, "%03x!!", retw); 
         Serial.print(rets);
      }
      else if(strcmp( str[0], "VER")==0){
        Serial.print(Version);
      }

      else {
        Serial.print("----!");        
      }
    }
    else { input_count++; }
  }
}

int atoi16( const char *NumberString )
{
    char *stopString;
    int result = strtol( NumberString, &stopString, 16 );
    return result;
}

#define NELEMS(arg) (sizeof(arg) / sizeof((arg)[0]))
