# Bit Write Safety

PLC communication libraries expose two different kinds of bit write. Choose the operation by the PLC data model, not by the wire representation.

## Semantic bit values

Typed bit-write APIs accept only the language's native Boolean value: `false`/`true`, `False`/`True`, or `bool`. Numbers such as `0` and `1`, strings, boxed values, and truthy/falsy objects are not semantic bit values. Parse configuration, CLI, or Node-RED input into an exact Boolean before calling a library API.

Raw frame and packed block-word APIs retain their documented wire-oriented inputs. They are not compatibility paths for typed Boolean writes.

## Prefer a native bit device

When the PLC program can use a native bit family, write that device directly. A direct bit write is one request and does not overwrite neighboring bits in a word.

## Bit inside a word

Use the explicitly named `WriteBitInWord` or `write_bit_in_word` helper only when the target is a bit stored inside a 16-bit word device. The helper performs exactly:

1. one complete-word read;
2. a local update of bit `0..15`; and
3. one complete-word write.

The write is sent after every successful read, even when the selected bit already has the requested value. The helper returns no computed or read-back value and performs no automatic verification, retry, route fallback, or resend.

Named and aggregate write APIs do not invoke this read-modify-write procedure implicitly. A word-bit address supplied to those APIs is rejected before transport; call the explicit helper after selecting the intended word route.

Where a library supports more than one complete-word route, use the helper for that specific route. The direct, relay, extended, qualified, or link-direct target is validated before the read and remains unchanged for the write. The helper never retries through another route or changes the destination automatically.

KEYENCE Host Link expansion-unit buffers use the route-specific `WriteBitInExpansionUnitBuffer` / `write_bit_in_expansion_unit_buffer` helper. It keeps the selected unit number and buffer address unchanged across one `URD` word read and one `UWR` word write; it is not an overload of the ordinary-device helper.

Operations on the same client cannot interleave between the read and write. This local FIFO ownership does not make the operation atomic at the PLC. PLC logic, another connection, or another controller can change the word after the read; the following complete-word write can overwrite that concurrent change.

Use PLC-side logic, a request/acknowledgement handshake, or exclusive ownership of the complete word when lost updates are unacceptable.

## Deadline and uncertain completion

FIFO queue waiting is outside the procedure timeout. After the helper becomes active, one absolute deadline covers the read, local update, write, and confirmed write response.

- A read failure or cancellation before the write sends no write.
- A complete PLC error response to the write is a definitive PLC rejection.
- Timeout, cancellation, close, transport loss, or malformed response after write transmission may have started means the PLC value is unknown.

For an unknown outcome, reconnect and read the target word before choosing the next application action. Do not automatically repeat the write: the first request may already have succeeded.

## Controlled use

Test state-changing operations on prepared development equipment. For production systems, select addresses and ownership rules deliberately, validate application input before the library call, and keep write-capable diagnostic tools separate from normal runtime operation.
