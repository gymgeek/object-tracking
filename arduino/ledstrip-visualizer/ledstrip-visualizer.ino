#include "FastLED.h"

// How many leds in your strip?
#define NUM_LEDS 90

// For led chips like Neopixels, which have a data line, ground, and power, you just
// need to define DATA_PIN.  For led chipsets that are SPI based (four wires - data, clock,
// ground, and power), like the LPD8806 define both DATA_PIN and CLOCK_PIN
#define DATA_PIN 3

// Define the array of leds
CRGB leds[NUM_LEDS];

byte led_intensities[NUM_LEDS];
int pos = 0;

void setup() { 
      Serial.begin(9600);
  	  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);

      for (int i = 0; i < NUM_LEDS; i++) {
        led_intensities[i] = 0;
      }
}


void dimLeds() {
  for (int i = 0; i < NUM_LEDS; i++) {
    led_intensities[i] = led_intensities[i] * 0.90;
  }
}

void showLeds() {
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB(led_intensities[i], led_intensities[i], led_intensities[i]);
  }
  FastLED.show();
}


void lightLeds(int position) {
  int lightWidth = (int) (NUM_LEDS / 15.0);

  int start = (int) (position - lightWidth / 2.0);
  
  for (int i = start; i < start + lightWidth; i++) {
    if (i >= 0 && i < NUM_LEDS) {
      led_intensities[i] = 255;
    }
  }
}


void loop() { 
 
  
  if (Serial.available()) {
    pos = Serial.read();
    lightLeds(pos);
  }

  showLeds();
  dimLeds();
  delay(30);

}
