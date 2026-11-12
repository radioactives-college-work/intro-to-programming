"""
Brightwater Leisure: Class Booking Cost Calculator.

Part of the Class and Facility Booking module. Works out the cost of a
block of class sessions for a member and prints a summary to the screen.
"""

BASE_PRICE = 8.00
PEAK_SURCHARGE = 2.00
MAX_DISCOUNT = 25
MEMBERSHIP_DISCOUNTS = {"standard": 0, "student": 10, "premium": 20}
TIME_SLOTS = ["peak", "off-peak"]


def get_whole_number(prompt, minimum, maximum):
    """Ask until the member enters a whole number in the allowed range.

    Args:
        prompt (str): the question to display.
        minimum (int): the lowest value allowed.
        maximum (int): the highest value allowed.

    Returns:
        int: the validated number.
    """
    while True:
        text = input(prompt).strip()
        if text.isdigit():
            value = int(text)
            #  12/11/2026 Corrected by JS | Needed to be <= the maximum to allow for the maximum to be entered.
            if minimum <= value <= maximum:
                # 12/11/2026 Corrected by JS | Needs to return value not text. Corrected to value
                return value
        print(f"Please enter a whole number from {minimum} to {maximum}.")


def get_choice(prompt, options):
    """Ask until the member types one of the allowed options.

    Args:
        prompt (str): the question to display.
        options (list): the accepted answers, in lower case.

    Returns:
        str: the chosen option, in lower case.
    """
    while True:
        text = input(prompt).strip().lower()
        if text in options:
            return text
        print("Please choose one of: " + ", ".join(options))


def calculate_subtotal(sessions, time_slot):
    """Return the cost of all sessions before any discount is taken off."""
    # 12/11/2026 Corrected by JS | Base price must be
    subtotal = sessions * BASE_PRICE
    if time_slot == "peak":
        subtotal = subtotal + PEAK_SURCHARGE
    return subtotal

# 12/11/2026 Corrected by JS | Added a colon after "(sessions):"
def session_discount(sessions):
    """Return the percentage discount for the number of sessions booked."""
    if sessions >= 10:
        return 10
    # 12/11/2026 Corrected by JS | Incorrectly unincludes the session number being 5 which should have a 5% discount.
    elif sessions >= 5:
        return 5
    return 0


def loyalty_discount(years):
    """Return the percentage discount for the years of membership."""
    if years >= 3:
        return 5
    return 0


def booking_band(total):
    """Return the booking size band for the total payable."""
    if total > 40:
        return "Large"
    elif total >= 20:
        return "Standard"
    return "Small"


def main():
    """Collect the booking details, work out the cost and show a summary."""
    name = input("Member name: ").strip()
    while name == "":
        name = input("Name cannot be empty. Member name: ").strip()
    membership = get_choice("Membership (standard/student/premium): ",
                            list(MEMBERSHIP_DISCOUNTS))
    sessions = get_whole_number("Number of sessions (1-12): ", 1, 12)
    time_slot = get_choice("Time slot (peak/off-peak): ", TIME_SLOTS)
    years = get_whole_number("Years of membership (0-50): ", 0, 50)

    # 12/11/2026 Corrected by JS | Added an underscore between time and slot to read time_slot rather than timeslot
    subtotal = calculate_subtotal(sessions, time_slot)
    member_pct = MEMBERSHIP_DISCOUNTS[membership]
    session_pct = session_discount(sessions)
    loyalty_pct = loyalty_discount(years)
    discount_pct = member_pct + session_pct + loyalty_pct
    discount_amount = subtotal * discount_pct / 100
    total = subtotal - discount_amount

    print()
    print("BOOKING SUMMARY")
    print("-" * 36)
    print(f"Member:              {name}")
    print(f"Subtotal:            £{subtotal:.2f}")
    print(f"Membership discount: {member_pct}%")
    print(f"Session discount:    {session_pct}%")
    print(f"Loyalty discount:    {loyalty_pct}%")
    print(f"Discount applied:    {discount_pct}%")
    print(f"Discount amount:     £{discount_amount:.2f}")
    print(f"Total payable:       £{total}")
    print(f"Booking size:        {booking_band(total)}")


if __name__ == "__main__":
    main()
