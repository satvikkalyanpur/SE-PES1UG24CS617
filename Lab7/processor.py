import math


def validate_height_and_fastpass(rider_spec):
    if not isinstance(rider_spec, str):
        return "Invalid rider specification. Use Height:FastPass."

    try:
        parts = rider_spec.strip().split(":")
        if len(parts) != 2:
            return "Invalid rider specification. Use Height:FastPass."

        height_str, pass_str = parts
        height = int(height_str.strip())
        pass_value = pass_str.strip().upper()

        if pass_value not in ("YES", "NO"):
            return "Invalid FastPass value. Enter YES or NO."

        eligible = height >= 120
        has_fastpass = pass_value == "YES"

        status = "FastPass Priority" if has_fastpass else "Standard Entry"
        decision = "Approved" if eligible else "Denied"

        return f"Height {height}cm: {decision} ({status})"

    except (ValueError, TypeError):
        return "Invalid rider specification. Use Height:FastPass."


def compute_dispatch_throughput(ride_metric_str):
    if not isinstance(ride_metric_str, str):
        return "Invalid ride metrics. Use riders/minutes."

    try:
        parts = ride_metric_str.strip().split("/")
        if len(parts) != 2:
            return "Invalid ride metrics. Use riders/minutes."

        riders = float(parts[0].strip())
        cycle_mins = float(parts[1].strip())

        if not math.isfinite(riders) or not math.isfinite(cycle_mins):
            return "Invalid ride metrics. Values must be finite."

        if riders < 0 or cycle_mins <= 0:
            return "Invalid ride metrics. Riders must be non-negative and minutes must be positive."

        rate = riders / cycle_mins
        return round(rate, 2)

    except (ValueError, TypeError, ZeroDivisionError):
        return "Invalid ride metrics. Use numeric riders/minutes."


def resolve_safety_restraint_code(zone_code):
    if not isinstance(zone_code, str):
        return "Invalid ride zone code."

    prefix = zone_code.strip().upper()[:3]

    restraint_types = {
        "CST": "Over-the-Shoulder Harness",
        "WTR": "Lap Bar and Seatbelt",
        "DRP": "Hydraulic Shoulder Vest",
        "WHL": "Manual Safety Bar"
    }

    if prefix not in restraint_types:
        return "Unknown ride zone code."

    return restraint_types[prefix]


def main():
    print("==== Running validate_height_and_fastpass ====")
    r_input = input("Enter rider spec (Height:FastPass, e.g. 140:YES): ")
    print(validate_height_and_fastpass(r_input))

    print("\n==== Running compute_dispatch_throughput ====")
    t_input = input("Enter riders/mins (e.g. 48/2.5): ")
    print("Throughput (riders/min):", compute_dispatch_throughput(t_input))

    print("\n==== Running resolve_safety_restraint_code ====")
    z_input = input("Enter ride zone code (e.g. CST_01, WTR_A): ")
    print("Restraint:", resolve_safety_restraint_code(z_input))


if __name__ == "__main__":
    main()