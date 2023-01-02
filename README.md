<p align="center"><img src="https://user-images.githubusercontent.com/466460/175758458-de1f65ca-8fb9-4519-a7af-9ed04d287399.png" width="125"></a>
<h1 align="center">NYC 311 Public Services Calendar</h1>
<h3 align="center">Home Assistant integration for New York City trash collection, school, and alternate side parking schedules.</h3>
<br />
<p align="center">
  <a href="https://www.codacy.com/gh/elahd/ha-nyc311/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=elahd/ha-nyc311&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/f0ea7693d5424bd6acabf70e8779dfa2"/></a>
  <a href="https://github.com/elahd/ha-nyc311/actions/workflows/hacs-validation.yaml"><img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/elahd/ha-nyc311/hacs-validation.yaml"></a>
  <a href="https://results.pre-commit.ci/latest/github/elahd/ha-nyc311/main"><img src="https://results.pre-commit.ci/badge/github/elahd/ha-nyc311/main.svg" /></a>
  <a href="https://github.com/elahd/ha-nyc311/commits/master"><img src="https://img.shields.io/github/commit-activity/y/elahd/ha-nyc311.svg" /></a>
  <a href="https://www.buymeacoffee.com/elahd"><img src="https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg"></a>
</p>
<p align="center">
  <a href="https://github.com/hacs/integration"><img src="https://img.shields.io/badge/HACS-Default-41BDF5.svg" /></a>
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Flauwbier.nl%2Fhacs%2Fnyc311" />
  <a href="https://github.com/elahd/ha-nyc311/releases"><img src="https://img.shields.io/github/release/elahd/ha-nyc311.svg" /></a>
  <a href="https://github.com/elahd/ha-nyc311/blob/main/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/elahd/ha-nyc311"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" /></a>
  <a href="https://github.com/PyCQA/pylint"><img src="https://img.shields.io/badge/linting-pylint-yellowgreen" /></a>
</p>

<hr />

## Screenshots

![nyc311-sensors](https://user-images.githubusercontent.com/466460/174864932-94dc72d8-b903-4448-b9c7-9868bd7282fa.png)

![nyc311-calendar](https://user-images.githubusercontent.com/466460/174862406-ba45d197-536c-422d-a13a-a9e7c1b6ebc4.png)

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

| Attribute Name | Example Value                                                       | Notes                                                                                                                                                                                |
| -------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Reason         | New Year's Day                                                      | Blank when service is normal.                                                                                                                                                        |
| Description    | Alternate side parking and meters are suspended for New Year's Day. |                                                                                                                                                                                      |
| Status         | Suspended                                                           | Shows standardized service statuses. The API returns a mess of statuses. These statuses fit the standard as defined in the nyc311calendar Python module.                             |
| Closure Type   | Exception                                                           | Shows "Exception" for special closures (holdays, etc.) and "Routine" for normal closures such as meter suspensions on Sundays. Field will be empty when service is running normally. |
| Service name   | Parking                                                             |                                                                                                                                                                                      |
| Date           | 2022-06-02                                                          |                                                                                                                                                                                      |

#### Date Sensors

| Attribute Name | Example Value                                                    | Notes                                                                                                                                                    |
| -------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Reason         | Rosh Hashanah                                                    | Field will be empty when service is operating normally.                                                                                                  |
| Description    | Public schools are closed for Winter Recess through December 31. | Shows full status.                                                                                                                                       |
| Status         | Suspended                                                        | Shows standardized service statuses. The API returns a mess of statuses. These statuses fit the standard as defined in the nyc311calendar Python module. |

## Calendars

This integration creates Home Assistant calendar entities for all three services.

## Requirements

You'll need an NYC API Portal developer account to use this library. It's free.

1. Sign up at <https://api-portal.nyc.gov/signup/>.
2. Log in, then subscribe to the "NYC 311 Public Developers" product at <https://api-portal.nyc.gov/products?api=nyc-311-public-api>. This subscription unlocks the calendar product.
3. Get your API key at <https://api-portal.nyc.gov/developer>. Either key (primary/secondary) will work.

**Component configuration is done via Home Assistant's integration's UI.** Enter your API key there during component setup.
