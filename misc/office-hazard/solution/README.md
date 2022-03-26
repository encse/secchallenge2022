# Office Hazard

Little known fact of the NTFS file system that files can store [alternate data](https://owasp.org/www-community/attacks/Windows_alternate_data_stream) next to their regular contents.

The hint that the challenge works only on NTFS immediately triggered this idea. WinRar extracted the archive to an NTFS folder. I went for command line tools to check what's hidden there. The file 'secret.txt', which reported 0 bytes in size, hid some binary content. I couldn't immediately find the way to extract that in powershell and finally used a [tool](https://www.nirsoft.net/utils/alternate_data_streams.html) to do that.

Running `strings` on the .exe revealed the flag `cd22{REDACTED}`

Many people have solved this challenge, it has been a really simple one.
