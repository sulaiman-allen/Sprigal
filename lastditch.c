// RFID Includes
#include <SPI.h>
#include <MFRC522.h>

// RFID Defines
#define RST_PIN    9
#define SS_PIN    10

bool printOnce = false;
const int NO_CARD_DETECTIONS_BEFORE_NEW_READ = 4;

MFRC522 mfrc522(SS_PIN, RST_PIN); // Create MFRC522 instance

int noCardCount = 0;

//push buttons
int prev = 6;
int toggle = 5;
int next = 4;

// variable for reading the pin status
int toggleVal = 0;
int prevVal = 0;
int nextVal = 0;

// temp variables for holding values for the last time they were checked
int toggleValLast = 0;
int prevValLast = 0;

int buttonState;

long lastDebounceTime = 0;
long debounceDelay = 50;

void setup() {
  // This is for Trinket 5V 16MHz
  #if defined (__AVR_ATtiny85__)
    if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
  #endif
  // End of trinket special code

  pinMode(prev, INPUT_PULLUP);
  pinMode(next, INPUT_PULLUP);
  pinMode(toggle, INPUT_PULLUP);    // declare pushbutton as input

  Serial.begin(9600); // Initialize serial communications with the PC
  while (!Serial); // Do nothing if no serial port is opened (needed for Arduinos based on ATMEGA32U4)
  SPI.begin(); // Init SPI bus
  mfrc522.PCD_Init(); // Init MFRC522
  Serial.println("Waiting for RFID-chip...");
}

void loop() {
  if (mfrc522.PICC_IsNewCardPresent()) {
    if(noCardCount > NO_CARD_DETECTIONS_BEFORE_NEW_READ) {
        getID();
    }

    noCardCount = 0;

  } else if (!mfrc522.PICC_IsNewCardPresent()) { // not present
    noCardCount++;
  }

  if (noCardCount < NO_CARD_DETECTIONS_BEFORE_NEW_READ) { // Read rfid tag continuously

      // read button states
      toggleVal = digitalRead(toggle);  // read input value
      prevVal = digitalRead(prev);
      nextVal = digitalRead(next);

       // because only one of these buttons should be able to be pressed each cycle though this loop, else if is used
       if (prevVal == LOW)
       {
         Serial.println("22222222");
         //delay(333);
       }
       else if (nextVal == LOW)
       {
         Serial.println("33333333");
       }

      printOnce = true;
      getID();
  }
  else {
    if(printOnce == true) {
      Serial.println("00000000");
      printOnce = false;
    }
  }
}

int getID() {
  byte readCard[4];
  if ( ! mfrc522.PICC_ReadCardSerial()) { //Since a PICC placed get Serial and continue
    printOnce = true;
    return -1;
  }
  if (mfrc522.PICC_IsNewCardPresent()) {
    printOnce = true;
    return -1;
  }
  
  for (int i = 0; i < mfrc522.uid.size; i++) {  // 
    readCard[i] = mfrc522.uid.uidByte[i];
    Serial.print(readCard[i], HEX);
  }
  Serial.println("");
}