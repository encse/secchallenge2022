# Broken

A customer just called. They dropped their Token Locker 3000, shattering both of its `1.3" SH1106 OLED ` displays. I have to go take care of some business, so I'm gonna need you to recover the data for them. You'll be able to do it, right?

I'm not sure whether you're familiar with the Token Locker 3000; it is a handheld crypto token protecting device. It has two screens on the two sides and two sets of keypads and buttons. When you start up the device, you have to enter two separate passwords, and if it checks out, it displays two QR codes containing the token. 

Unfortunately, we are out of replacement displays (damn supply chain shortages); thus, replacing them is not an option. However, I recorded the signals of the displays for you while the user entered their password (correctly, I hope), so you'll have to just work out how things work. The silkscreen labels of the display's pins are `GND`, `VCC`, `SDA`, `SCL`. 

*Note: The SH1106 is a cheap copy of the SSD1306. Depending on the resources you manage to find, you may need to use both's documentation, but keep in mind that they are not 100% identical.*

*Author: csf3r3ncz1*

## Inputs
- [challenge.sal](input/challenge.sal)

