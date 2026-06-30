# Bear With Me Solve Writeup

The provided image, `little-guy.jpg`, contains EXIF metadata.

Upload the image to an EXIF analysis tool such as <https://exifinfo.org/> or inspect it locally with a tool such as `exiftool`.

The relevant fields are:

```text
Camera Make: BearPhone
Camera Model: SuperPaw Pro
GPS Longitude: 6
GPS Latitude: 7
```

The challenge description gives the flag format:

```text
sgctf{CameraMake_CameraModel_LongitudeRounded_LatitudeRounded}
```

Remove spaces from field values when placing them in the flag. Substituting the extracted values gives:

```text
sgctf{BearPhone_SuperPawPro_6_7}
```
