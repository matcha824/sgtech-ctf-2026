# Important Notes

## Alternative to OpenCV

The challenge setup and solution uses OpenCV for image processing. PIL/Pillow was experimented with, but found that it required bitonal (grayscale) images and would not work with the below website.

When looking for online alternatives, this website was found to also solve the challenge: https://elysiatools.com/en/tools/image-boolean-xor

## Difficulty

The challenge hints at one-time pad reuse, which should be sufficient in guiding participants to search for why OTP reuse is problematic (see below). There is some variation in difficulty past understanding the vulnerability. The website is simple to use and provides a quick solution, though a script could be simple as well. However, there could be some other attempts (such as manually XORing the images per byte, or by using Pillow, which doesn't support RGB XOR) that would not work despite understanding the issue.

## Regarding the Automated Script and the Pad

The automated challenge setup script in /src randomly generates a new pad and subsequently creates the XOR'd images with that pad. The XOR'd images are already required for the challenge, but the associated pad is also included in the challenge repository, especially as a sanity check with the provided images (the automated script should generate the intended solution's output image as well).

Re-running the script will create/overwrite the following files:
- `pad.png`
- `picture_1.png`
- `picture_2.png`

Note that `picture_1.png` and `picture_2.png` are not in the `/src` folder. If XORing with the pad, you would need to ensure that you're using the correct pad with the images XOR'd with that specific pad. If the included `pad.png` is overwritten, the new `pad.png` would not work with the provided `picture_1.png` and `picture_2.png`.

However, this should largely be a non-issue for development as the challenge is able to be solved using the provided images without `pad.png`.