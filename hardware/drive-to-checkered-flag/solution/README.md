# Drive to checkered flag

Open the provided telemetry file in Wireshark. You will find two USB devices, one of them is a keyboard (address 5.4), the other one is an unknown device (5.3).

Filter for the second device with `usb.src == "5.3.2"` in Wireshark. 

![](wireshark.png)

If you look at the HID data (bottom) it resembles to the data of an XBOX controller, at least it stars with 0014... and has the right length. Is this the telemetry data of the wheel? 

We can show all the HID data in a column in Wireshark to make it more easy for the eye:
![](wireshark2.png)

Let's export this to a csv `File / Export Packet Dissections / As CSV...`.

If we put next to the video we can recognize that when the driver pushes buttons on the wheel the HID data changes. (I couldn't find this but after the contest I asked for help from the organizers.) 

It turns out that we need to check the low 4 bits of the second byte:

```
                  v
"14.905213","00140f00ff00000000000000ff18008000ff00ff"
"14.993223","00140f00ff00000000000000ff1a008000ff00ff"
"15.005272","00140f00ff00000000000000ff18008000ff00ff"
"15.033221","00140400ff00000000000000ff18008000ff00ff"
"15.073231","00140400ff00000000000000ff1a008000ff00ff"
"15.085227","00140400ff00000000000000ff18008000ff00ff"
"15.161234","00140f00ff00000000000000ff18008000ff00ff"
"15.173239","00140f00ff00000000000000ff1a008000ff00ff"
"15.213239","00140f00ff00000000000000ff18008000ff00ff"
"15.225263","00140f00ff00000000000000ff1a008000ff00ff"
                  ^
```

At 15.033221 it changes from f to 4 then quickly reset to f. Let's list all possible values:

```
> cat input.csv | awk -F '"' '{print substr($4, 6, 1)}' | uniq > signal
> cat signal | sort | uniq
0
4
f
```

I take the low 4 bits sort and uniq them. There are only 3 different values. `f` seems to be the separator between signals. Let's convert 4 -> 0 and 0 -> 1:

```
> cat signal | sed 's/f/ /' | sed 's/0/1/' | sed 's/4/0/' | tr -d '\n' > bits
> cat bits
 0 1 1 0 0 0 1 1 0 1 1 0 0 1 0 0 0 0 1 1 0 0 1 0 0 0 1 1 0 0 1 0 0 1 1 1 1 0 1 1 0 1 1 1 0 0 0 0 0 1 1 0 1 1 0 0 0 0 1 1 0 0 1 1 0 0 1 1 0 1 0 0 0 1 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 1 0 1 1 1 1 1 0 1 1 ... %
 ```

 It looks like ASCII code. In fact it is ASCII, and we can add some line wraps to make it more visible:

 ```
 > cat bits | sed -e "s/.\{16\}/&\n/g" > chars
 > cat chars
 0 1 1 0 0 0 1 1
 0 1 1 0 0 1 0 0
 0 0 1 1 0 0 1 0
 0 0 1 1 0 0 1 0
 0 1 1 1 1 0 1 1
 0 1 1 1 0 0 0 0
 0 1 1 0 1 1 0 0
 0 0 1 1 0 0 1 1
 0 0 1 1 0 1 0 0
 0 1 1 1 0 0 1 1
 0 0 1 1 0 0 1 1
 0 1 0 1 1 1 1 1
 ...
 ```

All is left is to convert it to ASCII chars to get the flag REDACTED.

