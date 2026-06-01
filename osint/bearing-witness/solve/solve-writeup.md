# Bearing Witness — Writeup

## Flag

```
sgctf{rsl3_nd5_gate_000}
```

## Solution

### 1. Identify the site type

The photo shows a fenced compound on flat plains: a gated paved drive, a low concrete building on the right, and a distinctive concrete tower set into an earthen berm/mound in the center-left of the frame. The combination of the squat tower on a mound, the dispersed support buildings, the heavy perimeter fence, and the warning signage points to Cold War missile infrastructure — specifically an anti-ballistic missile (ABM) launch facility rather than a Nike site or a Minuteman silo.

### 2. Narrow to Safeguard

The only operational U.S. ABM system that built this style of remote launch facility was the Stanley R. Mickelsen Safeguard Complex in Cavalier County, North Dakota. The main Missile Site Radar (MSR) is the famous pyramid at Nekoma, but Safeguard also fielded four Remote Sprint Launch (RSL) sites for perimeter defense: RSL-1, RSL-2, RSL-3, RSL-4.

### 3. Pick the right RSL

The Library of Congress HAER record for RSL-3 includes a photograph captioned:

> "Overall view from south to north of remote sprint launch site #3. Remote launch operations building on left, exclusion area sentry station at distant center, and limited area sentry station on right."

That caption matches the challenge image exactly:
- Remote launch operations building (with the tower/berm) on the **left**
- Exclusion area sentry station at the **distant center** along the drive
- Limited area sentry station on the **right**

So the site is **RSL-3**. The LoC record places it "North of State Route 5, approximately 10 miles Southwest of Walhalla, ND."

### 4. Identify the entrance and the road

RSL-3 sits on the north side of **North Dakota State Route 5 (ND-5)**. The paved drive in the photo is the main gate off ND-5 — i.e., the **ND-5 gate**. That gives the entrance identifier `nd5_gate`.

### 5. Bearing

The HAER caption already tells us the orientation: "view from south to north." Standing on ND-5 looking into the site, the camera faces due north. As a three-digit compass bearing that is **000**. This is verifiable in Google Street View at the RSL-3 entrance on ND-5.

### 6. Assemble the flag

```
site                  = rsl3
entrance_identifier   = nd5_gate
bearing               = 000

flag = sgctf{rsl3_nd5_gate_000}
```

## References

- LoC HAER, "Stanley R. Mickelsen Safeguard Complex, Remote Sprint Launch Site No. 3" — https://www.loc.gov/pictures/collection/hh/item/nd0090.photos.199480p/
- Wikipedia, "RSL-3" — https://en.wikipedia.org/wiki/RSL-3
- Wikipedia, "Stanley R. Mickelsen Safeguard Complex" — https://en.wikipedia.org/wiki/Stanley_R._Mickelsen_Safeguard_Complex
