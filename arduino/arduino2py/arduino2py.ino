/*
     ____________________________
    /                           /\
   /      Randy Boo13         _/ /\
  /                          / \/
 /                           /\
/___________________________/ /
\___________________________\/
 \ \ \ \ \ \ \ \ \ \ \ \ \ \ \

*/

#include <SPI.h>
#include <Wire.h>
#include <Adafruit_SSD1306.h>
/*
 * I2C ("Wire.h") OLED STUFF
*/
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 oled(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
Adafruit_SSD1306 oled2(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

/*
 * SPI DigiPots Setup
*/
byte address1 = B00010000;
byte address0 = B00000000;
byte incomingByte;
int ledPin = 33;


// Wire up the SPI Interface common lines:
#define SPI_CLOCK            13   //teensy   <->   SPI SCK (Pin 02 on MCP4261 DIP)
#define SPI_MOSI             11   //teensy   <->   SPI SDI (Pin 03 on MCP4261 DIP)
#define SPI_MISO             12   //teensy   <->   SPI SDO (Pin 13 on MCP4261 DIP)

#define btnA                 2
#define btnB                 3
#define btnX                 4
#define btnY                 5
#define btnDU                14
#define btnDD                17
#define btnDL                15
#define btnDR                16
#define btnSt                20
#define btnSe                10
#define btnLB                7
#define btnRB                6

// Then choose any other free pin as the Slave Select
#define SS_1 A7
#define SS_2 A8
#define SS_3 A9

// Timing Settings
int setupDelayTime = 2000;
int delayTime = 100;
int pressBtnTime = 200;


// Serial comm stuff
const byte buffSize = 80;
char inputBuffer[buffSize];
const char startMarker = '<';
const char endMarker = '>';
byte bytesRecvd = 0;
boolean readInProgress = false;
boolean newDataFromPC = false;

char messageFromPC[buffSize] = {0};
int newFlashInterval = 0;

unsigned long curMillis;

unsigned long prevReplyToPCmillis = 0;
unsigned long replyToPCinterval = 1000;


int aBtn = 0;
int bBtn = 0;
int xBtn = 0;
int yBtn = 0;
int lbBtn = 0;
int rbBtn = 0;
int duBtn = 0;
int ddBtn = 0;
int dlBtn = 0;
int drBtn = 0;
int ltBtn = 0;
int rtBtn = 0;
int LSx = 0;
int LSy = 0;
int RSx = 0;
int RSy = 0;
int startBtn = 0;
int selectBtn = 0;
int xboxBtn = 0;


//=============

void setup() {
  Serial.begin(9600);
  
  // Displays Setup
  oled.begin(SSD1306_SWITCHCAPVCC, 0x3D);
  oled2.begin(SSD1306_SWITCHCAPVCC, 0x3C);

  oled.clearDisplay();
  oled.setTextSize(2);
  oled.setTextColor(WHITE);
  oled.setCursor(0,0);
  oled.println(">");
  oled.display();

  oled2.clearDisplay();
  oled2.setTextSize(1);
  oled2.setTextColor(WHITE);
  oled2.setCursor(0,0);
  oled2.println("INPUT");
  oled2.println();
  oled2.setTextSize(2);
  oled2.println("< >");
  oled2.display();

  delay(delayTime);
  oled.clearDisplay();
  oled.display();

  // Setup DigiPot
  pinMode (SS_1, OUTPUT);
  pinMode (SS_2, OUTPUT);
  pinMode (SS_3, OUTPUT);
  SPI.begin();

  // Setup the pins
  pinMode(btnA, OUTPUT);
  pinMode(btnB, OUTPUT);
  pinMode(btnX, OUTPUT);
  pinMode(btnY, OUTPUT);
  pinMode(btnDU, OUTPUT);
  pinMode(btnDD, OUTPUT);
  pinMode(btnDL, OUTPUT);
  pinMode(btnDR, OUTPUT);
  pinMode(btnSt, OUTPUT);
  pinMode(btnSe, OUTPUT);
  pinMode(btnLB, OUTPUT);
  pinMode(btnRB, OUTPUT);

  digitalWrite(btnA, HIGH);
  digitalWrite(btnB, HIGH);
  digitalWrite(btnX, HIGH);
  digitalWrite(btnY, HIGH);
  digitalWrite(btnDU, HIGH);
  digitalWrite(btnDD, HIGH);
  digitalWrite(btnDL, HIGH);
  digitalWrite(btnDR, HIGH);
  digitalWrite(btnSt, HIGH);
  digitalWrite(btnSe, HIGH);
  digitalWrite(btnLB, HIGH);
  digitalWrite(btnRB, HIGH);

  delay(setupDelayTime);
  
}

//=============

void loop() {
  curMillis = millis();
  getDataFromPC();
  replyToPC();
}

//=============

void getDataFromPC() {

    // receive data from PC and save it into inputBuffer
    
  if(Serial.available() > 0) {

    char x = Serial.read();

      // the order of these IF clauses is significant
      
    if (x == endMarker) {
      readInProgress = false;
      newDataFromPC = true;
      inputBuffer[bytesRecvd] = 0;
      parseData();
    }
    
    if(readInProgress) {
      inputBuffer[bytesRecvd] = x;
      bytesRecvd ++;
      if (bytesRecvd == buffSize) {
        bytesRecvd = buffSize - 1;
      }
    }

    if (x == startMarker) { 
      bytesRecvd = 0; 
      readInProgress = true;
    }
  }
}

//=============
 
void parseData() {

    // split the data into its parts
    
  char * strtokIndx; // this is used by strtok() as an index
  
  strtokIndx = strtok(inputBuffer,",");      // get the first part - the string
//  strcpy(messageFromPC, strtokIndx);        // copy it to messageFromPC
  
//  strtokIndx = strtok(NULL, ",");          // this continues where the previous call left off
  aBtn = atoi(strtokIndx);     // convert this part to an integer
  
  strtokIndx = strtok(NULL, ","); 
  bBtn = atoi(strtokIndx);

  strtokIndx = strtok(NULL, ","); 
  xBtn = atoi(strtokIndx);

  strtokIndx = strtok(NULL, ","); 
  yBtn = atoi(strtokIndx);
  
  strtokIndx = strtok(NULL, ","); 
  lbBtn = atoi(strtokIndx);

  strtokIndx = strtok(NULL, ","); 
  rbBtn = atoi(strtokIndx);

  strtokIndx = strtok(NULL, ","); 
  duBtn = atoi(strtokIndx);

  strtokIndx = strtok(NULL, ","); 
  ddBtn = atoi(strtokIndx);

  strtokIndx = strtok(NULL, ","); 
  dlBtn = atoi(strtokIndx);
  
  strtokIndx = strtok(NULL, ","); 
  drBtn = atoi(strtokIndx);

  strtokIndx = strtok(NULL, ","); 
  ltBtn = atoi(strtokIndx);
  
  strtokIndx = strtok(NULL, ","); 
  rtBtn = atoi(strtokIndx);
  
  strtokIndx = strtok(NULL, ","); 
  LSx = atoi(strtokIndx);
  
  strtokIndx = strtok(NULL, ","); 
  LSy = atoi(strtokIndx);
  
  strtokIndx = strtok(NULL, ","); 
  RSx = atoi(strtokIndx);

  strtokIndx = strtok(NULL, ","); 
  RSy = atoi(strtokIndx);

  strtokIndx = strtok(NULL, ","); 
  startBtn = atoi(strtokIndx);
  
  strtokIndx = strtok(NULL, ","); 
  selectBtn = atoi(strtokIndx);
    
  strtokIndx = strtok(NULL, ","); 
  xboxBtn = atoi(strtokIndx);

  strtokIndx = strtok(NULL, ","); 
  pressBtnTime = atoi(strtokIndx);

  btnChecker();
}

//=============
void btnChecker() {
  if (aBtn >= 1){btnPress(btnA);}
  if (bBtn >= 1){btnPress(btnB);}
  if (xBtn >= 1){btnPress(btnX);}
  if (yBtn >= 1){btnPress(btnY);}
  //
  if (lbBtn >= 1){btnPress(btnLB);}
  if (rbBtn >= 1){btnPress(btnRB);}
  //
  if (duBtn >= 1){btnPress(btnDU);}
  if (ddBtn >= 1){btnPress(btnDD);}
  if (dlBtn >= 1){btnPress(btnDL);}
  if (drBtn >= 1){btnPress(btnDR);}
  //
  if (startBtn >= 1){btnPress(btnSt);}
  if (selectBtn >= 1){btnPress(btnSe);}
}


//=============

void btnPress(int pin) {
  // Pin goes LOW (it's pressed!)
  digitalWrite(pin, LOW);
  delay(pressBtnTime);
  
  // Pin goes high again
  digitalWrite(pin, HIGH);
  delay(delayTime);
  }
//=============

void digiPots(int addr, byte digiPotPinSelect, int pinVal)
{
  digitalWrite(addr, LOW);
  //
  SPI.transfer(digiPotPinSelect);
  SPI.transfer(pinVal);
//  delay(delayTime);
//  SPI.transfer(64);
  //
  digitalWrite(addr, HIGH);

}

//=============

void replyToPC() {

  if (newDataFromPC) {
    newDataFromPC = false;
  
    oled2.clearDisplay();
    oled2.setTextSize(1);
    oled2.setTextColor(WHITE);
    oled2.setCursor(0,0);
    oled2.println("<INPUT>");
    oled2.println();
    //
    oled2.setTextSize(2);
    oled2.print("A");
    oled2.setTextSize(1);
    oled2.print(aBtn);
    
    oled2.setTextSize(2);
    oled2.print(" B");
    oled2.setTextSize(1);
    oled2.print(bBtn);
    oled2.setTextSize(2);
    oled2.print(" X");
    oled2.setTextSize(1);
    oled2.print(xBtn);
    oled2.setTextSize(2);
    oled2.print(" Y");
    oled2.setTextSize(1);
    oled2.println(yBtn);
    //
    oled2.println();
    oled2.print("Lb ");
    oled2.print(lbBtn);
    oled2.print(" Rb ");
    oled2.print(rbBtn);
  
    //
    oled2.print(" Lt ");
    oled2.print(ltBtn);
    oled2.print(" Rt ");
    oled2.println(rtBtn);
    //
    oled2.print("Du ");
    oled2.print(duBtn);
    oled2.print(" Dd ");
    oled2.print(ddBtn);
    oled2.print(" Dl ");
    oled2.print(dlBtn);
    oled2.print(" Dr ");
    oled2.println(drBtn);
  
    //
    oled2.print("Lx ");
    oled2.print(LSx);
    oled2.print(" Ly ");
    oled2.print(LSy);
    oled2.print(" Rx ");
    oled2.print(RSx);
    oled2.print(" Ry ");
    oled2.println(RSy);
    //
    oled2.print("Start ");
    oled2.print(startBtn);
    oled2.print(" Se ");
    oled2.print(selectBtn);
    oled2.print(" Xbox ");
    oled2.print(xboxBtn);
    
    oled2.print(messageFromPC);
    oled2.display();
  }
}
