# Flagshift

There is not much to say about this challenge, we have the schematics of a logical circuit, and need to emulate it somehow. I went with Python because why not. I managed to wire the whole dataflow in the other direction first, and had to debug it for a while. I also didn't know what is the order of the bits. Is it LSB or MSB? Is it the same for the input and the seed?

But it was not hard to figure it out - once I realized that I reversed the order of the gates. With some trial and error I finally got the flag in binary, which had to be converted to ASCII chars of course.