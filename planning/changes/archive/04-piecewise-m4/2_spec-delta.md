# Spec delta: Temperature as a V in M4

## Capabilities touched

[specs/models.md](../../../specs/models.md)

## Changed

What changed:

| Item | From | To |
|---|---|---|
| M4's temperature terms | `tmax` and `tmin`, one straight slope each | For each temperature, the degrees below a knot and the degrees above it: `tmax_below`, `tmax_above`, `tmin_below`, `tmin_above` |
| Config | | `models.temperature_knots_c`: 21 for `tmax`, 18 for `tmin` |
| M1, M2, M3, M5, M6 | | Unchanged; their numbers are identical to the archive |
| M4's label in Table I | "PV + weather, linear" | Unchanged |

M4 stays one linear model, with four temperature terms in place of two.
