"""Convert IPv6 addresses between colon-hex text and 128-bit integers."""


from ipaddress import AddressValueError, IPv6Address


class IPv6FormatError(ValueError):
    """Raised when a string is not a valid IPv6 address.

    Subclassing ValueError keeps us compatible with code that already
    catches ValueError for malformed numeric input, while still letting
    callers narrow on IPv6FormatError when they want to distinguish
    address failures from other value errors.
    """


def ipv6_to_int(address: str) -> int:
    """Parse a colon-hex IPv6 string into its 128-bit integer.

    Delegating to ipaddress.IPv6Address gives us RFC 4291 parsing for
    free: leading zeros, embedded IPv4 (``::ffff:1.2.3.4``), and the
    ``::`` shorthand. We only wrap its error so callers catch one
    exception type regardless of how the string is malformed.
    """
    try:
        return int(IPv6Address(address))
    except AddressValueError as exc:
        raise IPv6FormatError(str(exc)) from exc


def int_to_ipv6(value: int) -> str:
    """Render a 128-bit integer as its canonical compressed IPv6 string.

    Canonical here means ipaddress' default text: lowercase hex, the
    longest run of zero groups replaced by ``::`` (ties go to the first
    run), and no leading zeros inside a group. The valid range is
    ``[0, 2**128 - 1]``.
    """
    if not isinstance(value, int):
        raise IPv6FormatError("value must be an int")
    if value < 0 or value >= (1 << 128):
        raise IPv6FormatError("integer out of range for an IPv6 address")
    return str(IPv6Address(value))
