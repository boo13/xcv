/*
 The receiving end of the xcv serial communication

 Project Name_ = arduino2python_serialCom
 Author__ = Randy "boo13" Bot
 Version__ = 0.1.4

      ____________________________
     /                           /\
    /      Randy Boo13         _/ /\
   /         v0.1.4           / \/
  /                           /\
 /___________________________/ /
 \___________________________\/
  \ \ \ \ \ \ \ \ \ \ \ \ \ \ \






*/

/* ========          Boiler-Plate             ===============
   ==========================================================
  
   ==========================================================
*/
#include <SPI.h>
#include <Wire.h>
#define SERIAL_BAUD 115200

/*
 * SPI DigiPots Setup
*/
byte address1 = B00010000;
byte address0 = B00000000;
byte incomingByte;

/* ========          Pins (Constants)         ===============
   ==========================================================
  
   ==========================================================
*/
#define ledPin 28

// Wire up the SPI Interface common lines:
#define SPI_CLOCK 13 //teensy   <->   SPI SCK (Pin 02 on MCP4261 DIP)
#define SPI_MOSI 11  //teensy   <->   SPI SDI (Pin 03 on MCP4261 DIP)
#define SPI_MISO 12  //teensy   <->   SPI SDO (Pin 13 on MCP4261 DIP)

// Buttons
#define btnA 2
#define btnB 3
#define btnX 4
#define btnY 5
#define btnDU 14
#define btnDD 17
#define btnDL 15
#define btnDR 16
#define btnSt 20
#define btnSe 10
#define btnLB 7
#define btnRB 6

// Then choose any other free pin as the Slave Select
#define SS_1 A7
#define SS_2 A8
#define SS_3 A9
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
Adafruit_SSD1306 display2(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
//==========================================================
//========    Serial Communication Stuff     ===============
//==========================================================
// Buffer size (less will chop off communication)
const byte buffSize = 80;
char inputBuffer[buffSize];
char messageFromPC[buffSize] = {0};

// Markers come from python List conversion
const char startMarker = '[';
const char endMarker = ']';

//
boolean clearMainDisplay = true;
boolean MainDisplay_fadeOn = true;
unsigned long MainDisplayTicker;

// TODO: Fix this call-response feature
String empty_response = "[0,0,0,0,0,0,0,0,0,0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0]";
//======================================================
//=============     Flags     ==========================
//======================================================
// Button Flags
int aBtn = 0;
int bBtn = 0;
int xBtn = 0;
int yBtn = 0;
int lbBtn = 0;
int rbBtn = 0;
int duBtn = 0;
int ddBtn = 0;
int dlBtn = 0;
int drBtn = 0; // 10 ints
float ltBtn = 0.0;
float rtBtn = 0.0;
float LSx = 0.0;
float LSy = 0.0;
float RSx = 0.0;
float RSy = 0.0; // 6 floats
int startBtn = 0;
int selectBtn = 0;
int xboxBtn = 0; // 3 ints
// 19 total in a "Button List"

// Display Flags
String last_command_sent;

// Serial Comm Flags
byte bytesRecvd = 0;
boolean readInProgress = false;
boolean newDataFromPC = false;


//______________  User Settings  ______________________//
// Adjust to your needs
boolean debug_mode = true;

//__________________  Timers  _________________________//
unsigned long curMillis;
unsigned long lastMillis;
unsigned long secCounter;

// Timing for xcontroller (button presses)
int delayTime = 100;
int pressBtnTime = 200;

//____________________________________________________//

/* =================     Setup     ==========================
   ==========================================================
   ==========================================================
   
*/
void setup() {
  Serial.begin(115200);

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C) or !display2.begin(SSD1306_SWITCHCAPVCC, 0x3D)) {
    Serial.println(F("SSD1306 allocation failed"));
  }

  // Clear the buffer
  display.clearDisplay();
  display2.clearDisplay();

  delay(1000);
  output_display("A");
  debug_display("B");
}

void loop() {
  curMillis = millis();
  getDataFromPC();
  replyToPC();
}

void output_display(String print_this) {
  display.clearDisplay();
  display.setTextSize(2); // Draw 2X-scale text
  display.setTextColor(WHITE);
  display.setCursor(10, 0);
  display.print("IN:");
  display.setCursor(30, 16);
  display.println(print_this);
  display.display();      // Show initial text
}


void debug_display(String print_this) {
  display2.clearDisplay();
  display2.setTextSize(2); // Draw 2X-scale text
  display2.setTextColor(WHITE);
  display2.setCursor(10, 0);
  display2.print("OUT:");
  display2.setCursor(30, 16);
  display2.println(print_this);
  display2.display();      // Show initial text
}


//=============

void getDataFromPC()
{

  // receive data from PC and save it into inputBuffer

  if (Serial.available() > 0)
  {

    char x = Serial.read();
    Serial1.print("INPUT: ");
    Serial1.println(x);
    //
    // the order of these IF clauses is significant
    //
    if (x == endMarker)
    {
      readInProgress = false;
      newDataFromPC = true;
      inputBuffer[bytesRecvd] = 0;
      parseData();
    }

    if (readInProgress)
    {
      inputBuffer[bytesRecvd] = x;
      bytesRecvd++;
      if (bytesRecvd == buffSize)
      {
        bytesRecvd = buffSize - 1;
      }
    }

    if (x == startMarker)
    {
      bytesRecvd = 0;
      readInProgress = true;
    }
  }
}

//=============
void replyToPC()
{

  if (newDataFromPC)
  {
    newDataFromPC = false;
    Serial.print(empty_response);
  }
}
//=============

void parseData()
{

  // split the data into its parts

  char *strtokIndx; // this is used by strtok() as an index
  //  strcpy(messageFromPC, strtokIndx);        // copy it to messageFromPC

  strtokIndx = strtok(inputBuffer, ","); // get the first part - the string
  aBtn = atoi(strtokIndx);               // convert this part to an integer

  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
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
void btnChecker()
{
  if (aBtn >= 1)
  {
    btnPress(btnA);
    Serial1.println("Pressing Button A");
  }
  if (bBtn >= 1)
  {
    btnPress(btnB);
    Serial1.println("Pressing Button B");
  }
  if (xBtn >= 1)
  {
    btnPress(btnX);
    Serial1.println("Pressing Button X");
  }
  if (yBtn >= 1)
  {
    btnPress(btnY);
    Serial1.println("Pressing Button Y");
  }
  if (lbBtn >= 1)
  {
    btnPress(btnLB);
    Serial1.println("Pressing Button LB");
  }
  if (rbBtn >= 1)
  {
    btnPress(btnRB);
    Serial1.println("Pressing Button RB");
  }
  if (duBtn >= 1)
  {
    btnPress(btnDU);
    Serial1.println("Pressing Button D Up");
  }
  if (ddBtn >= 1)
  {
    btnPress(btnDD);
    Serial1.println("Pressing Button D Down");
  }
  if (dlBtn >= 1)
  {
    btnPress(btnDL);
    Serial1.println("Pressing Button D Left");
  }
  if (drBtn >= 1)
  {
    btnPress(btnDR);
    Serial1.println("Pressing Button D Right");
  }
  if (startBtn >= 1)
  {
    btnPress(btnSt);
    Serial1.println("Pressing Button Start");
  }
  if (selectBtn >= 1)
  {
    btnPress(btnSe);
    Serial1.println("Pressing Button Select");
  }
}

//=============

void btnPress(int pin)
{
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
