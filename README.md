[![GitHub Workflow Status][builds-shield]][builds]
[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

# NYC 311 Public Services Calendar

## **Home Assistant integration for New York City trash collection, school, and alternate side parking schedules.**

## Sensors

This component sets up the sensors in the table below for each of the three tracked services (School, Trash, and Parking).

---

**✨ Entity _names_ for sensors showing day-of-week status update automatically. ✨**

This lets you easily create a card showing statuses for the week ahead without having to parse in names for days of the week.\*\*

---

This example is for schools as rendered on a Tuesday.

| Entity Name                      | Entity ID                             | Sensor Type     | Sensor Class | Description                                             |
| -------------------------------- | ------------------------------------- | --------------- | ------------ | ------------------------------------------------------- |
| Next School Closure<sup>\*</sup> | sensor.next_school_closure            | `sensor`        | `date`       | Next date on which school is closed. Excludes weekends. |
| School Yesterday<sup>\*</sup>    | binary_sensor.nyc311_school_yesterday | `binary_sensor` | `running`    | School status yesterday, just in case you missed it.    |
| School Today<sup>\*</sup>        | binary_sensor.nyc311_school_today     | `binary_sensor` | `running`    | School status today.                                    |
| School Tomorrow<sup>\*</sup>     | binary_sensor.nyc311_school_tomorrow  | `binary_sensor` | `running`    | School status tomorrow.                                 |
| School on Thursday               | binary_sensor.nyc311_school_in_2_days | `binary_sensor` | `running`    | School status 2 days from now.                          |
| School on Friday                 | binary_sensor.nyc311_school_in_3_days | `binary_sensor` | `running`    | School status 3 days from now.                          |
| School on Saturday               | binary_sensor.nyc311_school_in_4_days | `binary_sensor` | `running`    | School status 4 days from now.                          |
| School on Sunday                 | binary_sensor.nyc311_school_in_5_days | `binary_sensor` | `running`    | School status 5 days from now.                          |
| School on Monday                 | binary_sensor.nyc311_school_in_6_days | `binary_sensor` | `running`    | School status 6 days from now.                          |

\* Entity name does _not_ change dynamically.

In this example, on the following day, "School on Thursday" would be renamed "School on Friday", etc. Entity _IDs_ never change and are always named exactly as shown below.

### Binary Sensors: True vs False

The `binary_sensor`s are `running` sensors. This means that when the sensor is `on` or `True`, school is open, garbage is being collected, or alternate side parking rules are in effect. When the sensor is `off` or `False`, schools are closed and garbage collection or parking rules are suspended.

### Attributes

Each sensor has state attributes that give you more detail to play with using Jinja or template sensors.

## Requirements

You'll need an NYC API Portal developer account to use this library. It's free.

1. Sign up at https://api-portal.nyc.gov/signup/.
2. Log in, then subscribe to the "NYC 311 Public Developers" product at https://api-portal.nyc.gov/products?api=nyc-311-public-api. This subscription unlocks the calendar product.
3. Get your API key at https://api-portal.nyc.gov/developer. Either key (primary/secondary) will work.

**Component configuration is done via Home Assistant's integration's UI.** Enter your API key there during component setup.

[buymecoffee]: https://www.buymeacoffee.com/elahd
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/elahd/ha-nyc311.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/Maintainer-Elahd%20Bar--Shai%20%40elahd-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/elahd/ha-nyc311.svg?style=for-the-badge
[releases]: https://github.com/elahd/ha-nyc311/releases
[commits-shield]: https://img.shields.io/github/commit-activity/y/elahd/ha-nyc311.svg?style=for-the-badge
[commits]: https://github.com/elahd/ha-nyc311/commits/master
[builds-shield]: https://img.shields.io/github/workflow/status/elahd/ha-nyc311/HACS%20Validation.svg?style=for-the-badge
[builds]: https://github.com/elahd/ha-nyc311/actions/workflows/hacs-validation.yaml
