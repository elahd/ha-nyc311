"""Exercise rollover with real Home Assistant entity classes."""
from datetime import date, timedelta
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

from nyc311calendar import CalendarDayEntry, CalendarType, NYC311API, util
from nyc311calendar.services import Parking, ServiceType
from custom_components.nyc311.binary_sensor import DaysAheadSensor
from custom_components.nyc311.calendar import Calendar


def parking_entry(day, suspended=False):
    status = Parking.StatusType.SUSPENDED if suspended else Parking.StatusType.IN_EFFECT
    return CalendarDayEntry(
        service_profile=Parking.PROFILE,
        status_profile=Parking.STATUS_MAP[status],
        exception_reason="Veterans Day" if suspended else "",
        raw_description="Parking suspended" if suspended else "In effect",
        exception_summary="Parking Suspended (Veterans Day)" if suspended else "",
        date=day,
    )


class RolloverTests(TestCase):
    def test_today_and_two_days_advance_without_recreating_entities(self):
        days = {}
        for delta in range(-1, 9):
            day = date(2026, 11, 10) + timedelta(days=delta)
            days[day] = {service: parking_entry(day, day == date(2026, 11, 11))
                         for service in ServiceType}
        with patch.object(util, "today", return_value=date(2026, 11, 10)):
            initial = NYC311API._NYC311API__build_days_ahead(days)
        coordinator = SimpleNamespace(data={CalendarType.WEEK_AHEAD: initial}, config_entry=None)
        sensors = [DaysAheadSensor(coordinator, delta, initial[delta]["services"][ServiceType.PARKING])
                   for delta in (0, 2)]
        sensors[0].update_device_data()
        self.assertFalse(sensors[0].is_on)
        with patch.object(util, "today", return_value=date(2026, 11, 11)):
            coordinator.data[CalendarType.WEEK_AHEAD] = NYC311API._NYC311API__build_days_ahead(days)
        for sensor in sensors:
            sensor.update_device_data()
        self.assertTrue(sensors[0].is_on)
        self.assertEqual(sensors[0].extra_state_attributes["date"], "2026-11-11")
        self.assertEqual(sensors[1].extra_state_attributes["date"], "2026-11-13")

    def test_calendar_skips_yesterday_and_uses_exclusive_end(self):
        calendar = Calendar(SimpleNamespace(config_entry=None), ServiceType.PARKING)
        calendar._calendar = {date(2026, 11, day): parking_entry(date(2026, 11, day), True)
                              for day in (10, 11)}
        with patch("custom_components.nyc311.calendar.today", return_value=date(2026, 11, 11)):
            event = calendar.event
            self.assertEqual(event.start, date(2026, 11, 11))
            self.assertEqual(event.end, date(2026, 11, 12))
        with patch("custom_components.nyc311.calendar.today", return_value=date(2026, 11, 12)):
            self.assertIsNone(calendar.event)
