#include <OctoWS2811.h>

const int ledsPerStrip = 100; // 150;
const int strips = 8; // 4;

/*

    End of configuration

*/

const int totalLeds = ledsPerStrip * strips;

DMAMEM int displayMemory[ledsPerStrip*6];
int drawingMemory[ledsPerStrip*6];
byte readBuffer[totalLeds * 3];

const int config = WS2811_RGB | WS2811_800kHz;

OctoWS2811 leds(ledsPerStrip, displayMemory, drawingMemory, config);

void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(9600);
  Serial.setTimeout(50);
  leds.begin();
  leds.show();

  // Blink first led to show the program response
  for (int i = 0; i < 3; i++) {
    leds.setPixel(0, 0x00FF00);
    leds.show();
    delay(200);
    leds.setPixel(0, 0x000000);
    leds.show();
    delay(200);
  }

  clearLeds();
}

void loop() {

  int startChar = Serial.read();  // if so get the first byte

  if (startChar == '*') {
    digitalWrite(13, HIGH);
    unsigned int unusedField = 0;
    int count = Serial.readBytes((char *)&unusedField, 2);
    if (count != 2) {
      //Serial.println("Expected 2 bytes");
      return;
    }
    count = Serial.readBytes((char *)readBuffer, sizeof(readBuffer));
    if (count == sizeof(readBuffer)) {
      int dataIndex;
      byte r, g, b;
      for (int ledIndex = 0; ledIndex < totalLeds; ledIndex++) {
        dataIndex = ledIndex * 3;
        r = readBuffer[dataIndex];
        g = readBuffer[dataIndex + 1];
        b = readBuffer[dataIndex + 2];
        leds.setPixel(ledIndex, r, g, b);
      }
      leds.show();
      //Serial.println("Done!");
    } else {
      //Serial.println(count);
      //Serial.println(sizeof(readBuffer));
      //Serial.println("Not enough!");
    }
    
    digitalWrite(13, LOW);
  
  // we want the leds cleared
  } else if (startChar == '!') {
    clearLeds();
    Serial.println("Clearing leds");
  } else if (startChar == '?') {
    Serial.println("Here I can return some debug information");
  } else if (startChar >= 0) {
    // discard unknown characters
    Serial.println("I do not understant");
  }
}


void showLeds() {
  digitalWrite(13, HIGH);
  for (int i = 0; i < totalLeds; i++) {
    leds.setPixel(i, 0x003300);
  }
  leds.show();
  digitalWrite(13, LOW);
}


void clearLeds() {
  digitalWrite(13, HIGH);
  for (int i = 0; i < totalLeds; i++) {
    leds.setPixel(i, 0x000000);
  }
  leds.show();
  digitalWrite(13, LOW);
}
