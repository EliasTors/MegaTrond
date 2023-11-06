// Copilot:

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME680.h>

Adafruit_BME680 bme; // create BME680 object

void setup() {
    Serial.begin(9600);
    while (!Serial); // wait for serial port to connect
    if (!bme.begin(0x76)) {
        Serial.println(F("Could not find a valid BME680 sensor, check wiring!!"));
        while (1);
    }
    Serial.println("Temb,Pressure, humidity, gas");
}

void loop() {
    if (! bme.performReading()) {
        Serial.println("Failed to perform reading :(");
        return;
    }

    Serial.print(bme.temperature);
    Serial.print(",");
    Serial.print(bme.pressure / 100.0);
    Serial.print(",");
    Serial.print(bme.humidity);
    Serial.print(",");
    Serial.print(bme.gas_resistance / 1000.0);
    Serial.println();

    delay(1000);
}
