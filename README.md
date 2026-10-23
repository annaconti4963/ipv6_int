# ipv6_int

Convert IPv6 addresses between colon-hex string and packed 128-bit integer representations.

```python
from ipv6_int import ipv6_to_int, int_to_ipv6, IPv6FormatError

n = ipv6_to_int("2001:db8::1")       # 42540488161975842760550371480812562433
s = int_to_ipv6(n)                    # "2001:db8::1"

try:
    ipv6_to_int("not-an-address")
except IPv6FormatError:
    ...
```

## Why

Storing IPv6 addresses as text wastes space and makes range queries
awkward; storing the raw 128-bit integer makes indexing and comparison
trivial. This library is the thin, dependency-free adapter between
those two representations.

The trade-off: `int_to_ipv6` always returns the canonical compressed
form (lowercase, longest zero run collapsed to `::`). If you need to
preserve the original textual form — leading zeros, uppercase, or a
shorter `::` placement — round-tripping through the integer will not
do that. Store the original string separately if you need it.

## Edge cases

- Embedded IPv4 (`::ffff:1.2.3.4`) is accepted on input and rendered
  as pure hex on output.
- `int_to_ipv6(0)` returns `::` and `int_to_ipv6(1)` returns `::1`.
- Integers outside `[0, 2**128 - 1]` raise `IPv6FormatError`, as do
  malformed strings.
