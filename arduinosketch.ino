
 /*  Arduino to SL018/SL030 wiring:
 *  A3/TAG     1     5
 *  A4/SDA     2     3
 *  A5/SCL     3     4
 *  5V         4     -
 *  GND        5     6
 *  3V3        -     1
 */

#include <Wire.h>
#include <SL018.h>
#define TAG 17 // A3

SL018 rfid;
boolean printzeros = false;
boolean digiread = false;

//push buttons
int prev = 8;
int toggle = 9;
int next = 10;

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

void setup()
{
  Wire.begin();
  Serial.begin(9600);
  pinMode(TAG, INPUT);
  pinMode(prev, INPUT_PULLUP);
  pinMode(next, INPUT_PULLUP);
  pinMode(toggle, INPUT_PULLUP);    // declare pushbutton as input

}

void loop()
{
  // start seek mode
  rfid.seekTag();
  
  while(!digitalRead(TAG))
  {
     digiread = true;
     rfid.seekTag();
     // wait until tag detected
     if(!rfid.available() && digiread == true)
     {
       // print tag id
       Serial.println(rfid.getTagString());


       
       
       
       // the button presses are only going to need to exist while the tag is being read
       
       // read button states
       toggleVal = digitalRead(toggle);  // read input value
       prevVal = digitalRead(prev);
       nextVal = digitalRead(next);
       
       /*
       // check to see if the buttons were pressed (the input went from HIGH to LOW
       // and that enough time has gone by since the last press to ignore any noise
       
       // if the switch changed, due to noise or pressing:
       if(toggleVal != toggleValLast)
       {
        // reset the debouncing timer
         lastDebounceTime = millis(); 
       }
       
       if((millis() - lastDebounceTime) > debounceDelay)
       {
         // whatever the reading is at, its been there for longer than the debounce delay, so take it as its actual state
         
         //if the button state has changed:
         if (toggleVal != buttonState)
         {
           buttonState = toggleVal;
           
           //only allow the serial data to be transmitted if the new button state is LOW
           if (buttonState == LOW) // check if the input is LOW (button pressed)
           {       
             Serial.println("11111111");
           }
         } 
       }
       */
       
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
 
       
       // if the read is no longer happening
       if(digitalRead(TAG))
       {
         //break this loop
         digiread = false;
       }
     }
     printzeros = true;
  }
  if(printzeros == true)
  {
    Serial.println("00000000");
    //delay(200);
    printzeros = false;
  }
}

