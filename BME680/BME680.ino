// Copilot:

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME680.h>
int lyd = A0;
int lys = A1;
Adafruit_BME680 bme; // create BME680 object

void setup() {
    pinMode(lyd,INPUT);
    pinMode(lys, INPUT);
    Serial.begin(9600);
    while (!Serial); // wait for serial port to connect
    if (!bme.begin(0x76)) {
        Serial.println(F("Could not find a valid BME680 sensor, check wiring!!"));
        while (1);
    }
    Serial.println("Temp,Pressure, humidity, gas, lyd, lys");
}

void loop() {
    int lydniva = analogRead(lyd);
    int lysniva = analogRead(lys);
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
    Serial.print(",");
    Serial.print(lydniva);
    Serial.print(",");
    Serial.print(lysniva);
    Serial.println();

    delay(1000);
}
