# Changelog for Renoweb Home Assistant Integration

## Version 0.1.16 (NOT RELEASED)

- `FIXED`: Ensuring all Unit of Measurrement are always the same (dage). This ensures that the sensors can be used with Helpers like the Min/Max helper.
- `ADDED`: Added new sensor called `sensor.renoweb_days_until_next_pickup`, which shows the number of days until the next pick-up of any of the containers.

## Version 0.1.15

- `FIXED`: Fixing deprecated `async_get_registry` that might start showing up in HA 2022.6

## Version 0.1.14

* `FIXED`: Fixes issue #10, with a deprecation warning about `device_state_attributes`.

## Version 0.1.13

* `FIXED`: **BREAKING CHANGE** Det viser sig at i nogle kommuner vil der forekomme afhentninger der hedder det samme - eksempelvis Haveaffald - men forekommer på forskellige tidspunkter. Hvis såddane forkommer, så ville kun den sidste af disse blive registreret. Denne version løser dette problem, ved at tilføje et unikt id til navnet. Men ved at gøre dette, så bryder det med tidligere versioner, som kun genererede et unikt id baseret på type. Så når man har opdateret til denne version, er det nødvendigt at:
  * Slette integration, fra *Integrations* siden og derefter tilføje den igen.
  * Rette på de sider hvor man viser sensorerne da de nu, for de flestes vedkommende, har fået nye navne
  * Rette i eventuelle automatiseringer, som anvender disse sensorer, af samme årsag som ovenfor.

  Beklager dette, men det er den eneste måde at sikre at alle data vises for alle.
  Fixer issue #7
* `FIXED`: Tilføjet **iot_class** til `manifest.json`, som krævet af Home Assistant fra version 2021.5

## Version 0.1.12-Beta

* `FIXED`: BREAKING CHANGE Det viser sig at i nogle kommuner vil der forekomme afhentninger der hedder det samme - eksempelvis Haveaffald - men forekommer på forskellige tidspunkter. Hvis såddane forkommer, så ville kun den sidste af disse blive registreret. Denne version løser dette problem, ved at tilføje et unikt id til navnet. Men ved at gøre dette, så bryder det med tidligere versioner, som kun genererede et unikt id baseret på type. Så når man har opdateret til denne version, er det nødvendigt at:
  * Slette integration, fra *Integrations* siden og derefter tilføje den igen.
  * Rette på de sider hvor man viser sensorerne da de nu, for de flestes vedkommende, har fået nye navne
  * Rette i eventuelle automatiseringer, som anvender disse sensorer, af samme årsag som ovenfor.

  Beklager dette, men det er den eneste måde at sikre at alle data vises for alle.