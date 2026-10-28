"""Manage bookings for fitness classes and export their rosters."""

import json
import os
from pathlib import Path

CLASS_CAPACITY = {"Yoga": 3, "HIIT": 2, "Spin": 4}
rosters = {}


def book_class(member_id, class_name, attendance_log=None):
    """Book a member into a class if a seat is available."""
    if class_name not in CLASS_CAPACITY:
        print("Unknown class:", class_name)
        return False
    class_roster = rosters.setdefault(class_name, [])
    if len(class_roster) >= CLASS_CAPACITY[class_name]:
        print("Class full:", class_name)
        return False
    class_roster.append(member_id)
    if attendance_log is not None:
        attendance_log.append(f"{member_id} -> {class_name}")
    return True


def cancel_booking(member_id, class_name):
    """Cancel a member's booking, reporting a missing booking clearly."""
    class_roster = rosters.get(class_name)
    if class_roster is None or member_id not in class_roster:
        print("Nothing to cancel")
        return False
    class_roster.remove(member_id)
    return True


def set_capacity(class_name, seats):
    """Set a class capacity to a non-negative integer."""
    if not isinstance(seats, int) or isinstance(seats, bool) or seats < 0:
        raise ValueError("Capacity must be a non-negative integer")
    CLASS_CAPACITY[class_name] = seats


def add_members(class_name, count):
    """Add numbered walk-in guests to a class."""
    if not isinstance(count, int) or isinstance(count, bool) or count < 0:
        raise ValueError("Guest count must be a non-negative integer")
    for guest_number in range(count):
        book_class(f"GUEST-{guest_number}", class_name)


def export_roster(file_path="gym_schedule.json"):
    """Write all current rosters as JSON to the requested path."""
    with Path(file_path).open("w", encoding="utf-8") as roster_file:
        json.dump(rosters, roster_file, indent=2)


def clear_old_exports(prefix="old_"):
    """Remove matching JSON exports from the current directory."""
    os.system("rm -f " + prefix + "*.json")


def show_rosters():
    """Print each class and its current members."""
    for class_name, members in rosters.items():
        print(class_name, ":", ", ".join(str(member) for member in members))


def main():
    """Run the sample booking workflow and prompt for walk-ins."""
    book_class("M1", "Yoga")
    book_class("M2", "Yoga")
    book_class("M3", "Yoga")
    book_class("M4", "Yoga")
    book_class(55, "HIIT")
    book_class("M5", "Pilates")
    set_capacity("Spin", 0)
    add_members("Spin", 3)
    cancel_booking("M9", "Boxing")
    guest_input = input("How many walk-in guests for HIIT? (Enter for 1): ") or "1"
    try:
        guest_count = int(guest_input)
        add_members("HIIT", guest_count)
    except ValueError:
        print("Please enter a non-negative whole number.")
    clear_old_exports()
    export_roster()
    show_rosters()


if __name__ == "__main__":
    main()
