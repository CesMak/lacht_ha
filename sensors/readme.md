
# Tasmota Zistern

# Eltako
## Setup
* ELTAKO DSZ15DE 3×80
![alt text](docs/image.png)

Schnittstelle Impulsausgang S0 nach DIN EN 62053-31,
potenzialfrei durch einen Optokoppler,
max. 30V DC/2OmA u. min.5V DC.
Impedanz 100 Ohm,
Impulslänge 30ms, 1000Imp./kWh

Der im Datenblatt erwähnte Optokoppler sitzt bereits im Zähler. Du kannst dir die zwei Anschlüsse vorstellen wie zwei Pins eines Tasters, der alle X kWh gedrückt wird. Ich habe einen der Pins mit GNS (Masse, Minus, Null, Erde) verbunden und den anderen mit einem GPIO des Raspberry. Damit “nicht gedrückt” aber ein definiertes Signal gibt, muss man den Pin am GPIO des Raspberry noch auf 3,3V (niemals 5V) “ziehen”. Dazu nutzt man einen Wiserstand mit 10 kOhm (10000 Ohm) oder mehr. Wenn jetzt der gedankliche “Taster gedrückt” wird, liegen kurz am GPIO des Raspberry das GND-Signal an statt wie sonst die 3,3 V. Diese “negative Flanke” kann man registrieren und zählen. Und das macht der Volkszähler für dich.

Wichtig ist nur, dass dir dein Datenblatt sagt, welcher der beiden Anschlüsse am Zähler an “GND” muss. Sonst funktioniert der Aufbau nicht.

## TODO:
* Was ist vzlogger, volkszaehler etc.?


## Links:
* [ELTAKO DSZ15DE 3×80](https://www.eltako.com/fileadmin/downloads/de/datenblatt/Datenblatt_DSZ15DE-3x80A.pdf)
* https://go-seven.de/2021/07/stromzaehler-mit-s0-impulsausgang-an-raspberry-pi-mit-volkszaehler-auswerten/
* https://github.com/volkszaehler/vzlogger
* [Pi Pico MQTT Code](https://www.youtube.com/watch?v=6ZsRfKReKIc&t=2s)