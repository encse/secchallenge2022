# falleen system
Let's start with a quick check on the binary:
```shell
> file magnetic-tape.dd
magnetic-tape.dd: DOS/MBR boot sector; partition 1 : ID=0xee, start-CHS (0x0,0,2), end-CHS (0x3ff,255,63), startsector 1, 40959 sectors, extended partition table (last)
> binwalk magnetic-tape.dd

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
1048576       0x100000        LUKS_MAGIC sha256
5860218       0x596B7A        MySQL ISAM compressed data file Version 6
```

It seems that it's a LUKS encrypted file. I spinned up a Linux machine and followed a tutorial to create a loop device from the .dd file, then decrypt with `cryptsetup`.

```
> sudo losetup --partscan --find --show magnetic-tape.dd
/dev/loop0
> sudo cryptsetup luksOpen /dev/loop0p1 img
Enter passphrase for /dev/loop0p1:
```

Ooops we need a password. Let's look around in the binary:
```shell
> strings magnetic-tape.dd
....
BS`Y
The key is:REDACTED
EFI PART
```

Ok we seem to have a key, let's try again. No luck, try again, no luck, try similar password, no luck, try empty password, nope... I just couldn't get over this... I talked to the organizers and it has turned out that my tiny AWS Linux machine didn't have enough RAM... I had the right password all the time, but it returned an error because of running out of memory. Ouch....

Anyway. After the short detour (like 8 hours), `cryptsetup` finally ran successfully and created a new file under `/dev/mapper/img` for me.

I could mount it as a filesystem, but... it was empty...

```shell
$ mkdir /mnt/img
$ mount img /mnt/img
$ ls -la /mnt/img
lost+found
```

I went back to the decrypted img file, and ran strings again, because who knows, and all of the sudden it has found the flag:

```shell
$ strings img | grep cd22
cd22{REDACTED}
```

I talked to the author of the challenge again and it turns it was an oversight on his end. The flag should not be plain visible. I was expected to recover a deleted Linux binary and reverse engineer that...

`¯\_(ツ)_/¯`