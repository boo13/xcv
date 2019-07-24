/*
 The receiving end of the xcv serial communication

 Project Name_ = arduino2python_serialCom
 Author__ = Randy "boo13" Bot
 Version__ = 0.1.1

      ____________________________
     /                           /\
    /      Randy Boo13         _/ /\
   /         v0.1.1           / \/
  /                           /\
 /___________________________/ /
 \___________________________\/
  \ \ \ \ \ \ \ \ \ \ \ \ \ \ \






*/

/* ========          Boiler-Plate             ===============
   ==========================================================
  
   ==========================================================
   
*/
//Libraries
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_SSD1306.h>

/*
 * Serial
*/
#define SERIAL_BAUD 115200

/*
 * I2C ("Wire.h")
*/
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define OLED_RESET -1 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 oled_main(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
Adafruit_SSD1306 oled_debug(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

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

//==========================================================
//========    Serial Communication STuff     ===============
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

//int newFlashInterval = 0;
//unsigned long prevReplyToPCmillis = 0;
//unsigned long replyToPCinterval = 1000;

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
void setup()
{
  Serial.begin(SERIAL_BAUD);
  Serial4.begin(SERIAL_BAUD); // For debugging

  //==============================//
  //
  // SETUP the displays
  //
  oled_main.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  oled_debug.begin(SSD1306_SWITCHCAPVCC, 0x3D);

  clearDisplays();

  drawDisplayHeaders();

  oled_debug.setTextSize(2);
  oled_debug.println("[ ... ]");

  displayDisplays();
  //
  //==============================//
  // SETUP the DigiPot pins
  //
  pinMode(SS_1, OUTPUT);
  pinMode(SS_2, OUTPUT);
  pinMode(SS_3, OUTPUT);
  SPI.begin();
  //
  // SETUP the pins
  //
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
  //
  // SET pins HIGH
  //
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
  //
  // Chill...
  delay(2000);
}

//======================================================
//=============     Loop      ==========================
//======================================================
void loop()
{
  curMillis = millis();

  if (MainDisplayTicker >= 1000)
  {
    lastMillis = MainDisplayTicker;
    MainDisplayTicker = 0;
    secCounter++;
  }
  else
  {
    MainDisplayTicker = curMillis - lastMillis;
  }

  // Debug check
  if (debug_mode == true)
  {
    debug_mode_show();
  }

  getDataFromPC();
  replyToPC();
}

//=============

void getDataFromPC()
{

  // receive data from PC and save it into inputBuffer

  if (Serial.available() > 0)
  {

    char x = Serial.read();

    // // Optional debugging on Serial4
    // if (Serial4.available())
    // {
    //   Serial4.print("INPUT: ");
    //   Serial4.println(x);
    // }

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
    drawMainDisplay("A");
  }
  if (bBtn >= 1)
  {
    btnPress(btnB);
    drawMainDisplay("B");
  }
  if (xBtn >= 1)
  {
    btnPress(btnX);
    drawMainDisplay("X");
  }
  if (yBtn >= 1)
  {
    btnPress(btnY);
    drawMainDisplay("Y");
  }
  //
  if (lbBtn >= 1)
  {
    btnPress(btnLB);
    drawMainDisplay("LB");
  }
  if (rbBtn >= 1)
  {
    btnPress(btnRB);
    drawMainDisplay("RB");
  }
  //
  if (duBtn >= 1)
  {
    btnPress(btnDU);
    drawMainDisplay("DU");
  }
  if (ddBtn >= 1)
  {
    btnPress(btnDD);
    drawMainDisplay("DD");
  }
  if (dlBtn >= 1)
  {
    btnPress(btnDL);
    drawMainDisplay("DL");
  }
  if (drBtn >= 1)
  {
    btnPress(btnDR);
    drawMainDisplay("DR");
  }
  //
  if (startBtn >= 1)
  {
    btnPress(btnSt);
    drawMainDisplay("St");
  }
  if (selectBtn >= 1)
  {
    btnPress(btnSe);
    drawMainDisplay("Se");
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

//=============

void updateDisplays()
{
  //
  clearDisplays();
  //
  drawDisplayHeaders();
  //
  drawDebugDisplay();
  //
  drawMainDisplay(" ");
  //
  displayDisplays();
}

//=============

void replyToPC()
{

  if (newDataFromPC)
  {
    updateDisplays();
    newDataFromPC = false;
    Serial.print(empty_response);
  }
}

//=========================================================================================
//=========================================================================================
//============= DISPLAY utils
//=========================================================================================
//=========================================================================================
void clearDisplays()
{
  oled_debug.clearDisplay();
  oled_main.clearDisplay();
}

void drawDisplayHeaders()
{
  oled_main.display();
  oled_main.setTextSize(2);
  oled_main.setTextColor(WHITE);
  oled_main.setCursor(48, 0);
  oled_main.println("XCV");
  //
  oled_debug.setTextSize(2);
  oled_debug.setTextColor(WHITE);
  oled_debug.setCursor(0, 0);
  oled_debug.print("INPUT ");
  oled_debug.setTextSize(1);
  oled_debug.println("< debug >");
  oled_debug.setCursor(0, 16);
}

void drawMainDisplay(String input)
{
  if (input != " ")
  {
    last_command_sent = input;
    oled_main.setCursor(52, 24);
    oled_main.setTextSize(5);
    oled_main.println(last_command_sent);
  }
}

void drawDebugDisplay(String input)
{
  oled_debug.setTextSize(2);
  oled_debug.setCursor(0, 16);

  oled_debug.print("A");
  oled_debug.setTextSize(1);
  oled_debug.print(aBtn);

  oled_debug.setTextSize(2);
  oled_debug.print(" B");
  oled_debug.setTextSize(1);
  oled_debug.print(bBtn);
  oled_debug.setTextSize(2);
  oled_debug.print(" X");
  oled_debug.setTextSize(1);
  oled_debug.print(xBtn);
  oled_debug.setTextSize(2);
  oled_debug.print(" Y");
  oled_debug.setTextSize(1);
  oled_debug.println(yBtn);
  //
  oled_debug.println();
  oled_debug.print("Lb ");
  oled_debug.print(lbBtn);
  oled_debug.print(" Rb ");
  oled_debug.print(rbBtn);

  //
  oled_debug.print(" Lt ");
  oled_debug.print(ltBtn);
  oled_debug.print(" Rt ");
  oled_debug.println(rtBtn);
  //
  oled_debug.print("Du ");
  oled_debug.print(duBtn);
  oled_debug.print(" Dd ");
  oled_debug.print(ddBtn);
  oled_debug.print(" Dl ");
  oled_debug.print(dlBtn);
  oled_debug.print(" Dr ");
  oled_debug.println(drBtn);

  //
  oled_debug.print("Lx ");
  oled_debug.print(LSx);
  oled_debug.print(" Ly ");
  oled_debug.print(LSy);
  oled_debug.print(" Rx ");
  oled_debug.print(RSx);
  oled_debug.print(" Ry ");
  oled_debug.println(RSy);
  //
  oled_debug.print("Start ");
  oled_debug.print(startBtn);
  oled_debug.print(" Se ");
  oled_debug.print(selectBtn);
  oled_debug.print(" Xbox ");
  oled_debug.print(xboxBtn);
}

void displayDisplays()
{
  oled_debug.display();
  oled_main.display();
}

void debug_mode_show()
{
  Serial4.print("Second Counter: ");
  Serial4.println(secCounter);
}
