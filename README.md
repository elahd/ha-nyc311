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

That is, on a Tuesday, the `binary_sensor.nyc311_school_exception_in_2_days` sensor will be named `School Exception on Thursday`. On a Wednesday, that same sensor will be named `School Exception on Friday`. This lets you easily create a card showing statuses for the week ahead without having to parse in names for days of the week.

---

This example is for schools as rendered on a Tuesday.

| Entity Name                             | Entity ID                                       | Sensor Type     | Sensor Class | Description                                             |
| --------------------------------------- | ----------------------------------------------- | --------------- | ------------ | ------------------------------------------------------- |
| Next School Exception<sup>\*</sup>      | sensor.next_school_exception                    | `sensor`        | `date`       | Next date on which school is closed. Excludes weekends. |
| School Exception Yesterday<sup>\*</sup> | binary_sensor.nyc311_school_exception_yesterday | `binary_sensor` | `None`       | School status yesterday, just in case you missed it.    |
| School Exception Today<sup>\*</sup>     | binary_sensor.nyc311_school_exception_today     | `binary_sensor` | `None`       | School status today.                                    |
| School Exception Tomorrow<sup>\*</sup>  | binary_sensor.nyc311_school_exception_tomorrow  | `binary_sensor` | `None`       | School status tomorrow.                                 |
| School Exception on Thursday            | binary_sensor.nyc311_school_exception_in_2_days | `binary_sensor` | `None`       | School status 2 days from now.                          |
| School Exception on Friday              | binary_sensor.nyc311_school_exception_in_3_days | `binary_sensor` | `None`       | School status 3 days from now.                          |
| School Exception on Saturday            | binary_sensor.nyc311_school_exception_in_4_days | `binary_sensor` | `None`       | School status 4 days from now.                          |
| School Exception on Sunday              | binary_sensor.nyc311_school_exception_in_5_days | `binary_sensor` | `None`       | School status 5 days from now.                          |
| School Exception on Monday              | binary_sensor.nyc311_school_exception_in_6_days | `binary_sensor` | `None`       | School status 6 days from now.                          |

\* Entity name does _not_ change dynamically.

In this example, on the following day, "School Exception on Thursday" would be renamed "School Exception on Friday", etc. Entity _IDs_ never change and are always named exactly as shown below.

### Binary Sensors: True vs False

The `binary_sensor`s are generic on/off binary sensors that show whether there is a service exception on a given day. This means that when the sensor is `on` or `True`, school is closed, garbage is not being collected, or alternate side parking rules are suspended. When the sensor is `off` or `False`, services are operating normally. Note that things like school closures on weekends are considered "normal" and will not be flagged as exceptions.

Service icons have a slash through them when sensors are `on`. This may be counter-intuitive, but the goal is to show that there is no service on that day.

### Attributes

Each sensor has state attributes that give you more detail to play with using Jinja or template sensors.

#### Binary Sensors

| Attribute Name  | Example Value                                                       | Notes                                                                                                                                                  |
| --------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Reason          | New Year's Day                                                      | Blank when service is normal.                                                                                                                          |
| Description     | Alternate side parking and meters are suspended for New Year's Day. |                                                                                                                                                        |
| Status          | Suspended                                                           | Shows full status. For example, for schools, this will show "Closed" on weekends, even though this add-in doesn't mark weekend closures as exceptions. |
| Routine closure | false                                                               | Shows true for "normal" service suspensions, such as school closures on weekends.                                                                      |
| Service name    | Parking                                                             |                                                                                                                                                        |

#### Date Sensors

| Attribute Name | Example Value                                                    | Notes              |
| -------------- | ---------------------------------------------------------------- | ------------------ |
| Reason Winter  | Recess                                                           |                    |
| Description    | Public schools are closed for Winter Recess through December 31. | Shows full status. |
| Status         | Closed                                                           |                    |

## Requirements

You'll need an NYC API Portal developer account to use this library. It's free.

1. Sign up at https://api-portal.nyc.gov/signup/.
2. Log in, then subscribe to the "NYC 311 Public Developers" product at https://api-portal.nyc.gov/products?api=nyc-311-public-api. This subscription unlocks the calendar product.
3. Get your API key at https://api-portal.nyc.gov/developer. Either key (primary/secondary) will work.

**Component configuration is done via Home Assistant's integration's UI.** Enter your API key there during component setup.

[buymecoffee]: https://www.buymeacoffee.com/elahd
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Default-41BDF5.svg
[license-shield]: https://img.shields.io/github/license/elahd/ha-nyc311.svg
[maintenance-shield]: https://img.shields.io/badge/Maintainer-Elahd%20Bar--Shai%20%40elahd-blue.svg
[releases-shield]: https://img.shields.io/github/release/elahd/ha-nyc311.svg
[releases]: https://github.com/elahd/ha-nyc311/releases
[commits-shield]: https://img.shields.io/github/commit-activity/y/elahd/ha-nyc311.svg
[commits]: https://github.com/elahd/ha-nyc311/commits/master
[builds-shield]: https://img.shields.io/github/workflow/status/elahd/ha-nyc311/HACS%20Validation.svg
[builds]: https://github.com/elahd/ha-nyc311/actions/workflows/hacs-validation.yaml
