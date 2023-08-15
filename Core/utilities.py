def format_to_inr(amount):
    is_negative = True if amount < 0 else False
    is_zero = True if amount == 0 or amount is None else False

    if is_zero:
        return "₹" + str(0)

    if is_negative:
        amount = abs(amount)

    def truncate_float(number, places):
        return int(number * (10**places)) / 10**places

    if amount < 1e3:
        result = amount

    if 1e3 <= amount < 1e5:
        result = str("{:,.2f}".format(truncate_float((amount / 1e5) * 100, 2))) + " K"

    if 1e5 <= amount < 1e7:
        result = str("{:,.2f}".format(truncate_float((amount / 1e7) * 100, 2))) + " L"

    if amount > 1e7:
        result = str("{:,.2f}".format(truncate_float(amount / 1e7, 2))) + " Cr"

    if is_negative:
        result = "-" + str(result)

    return "₹" + str(result)
