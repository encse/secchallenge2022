# Office Hazard

Little known fact of the NTFS file system that files can store [alternate data](https://owasp.org/www-community/attacks/Windows_alternate_data_stream) next to their regular contents.

The hint that the challenge works only on NTFS immediately triggered this idea. I used WinRar and extracted the archive to an NTFS folder. Went for command line tools to check what's hidden there. I found that the file 'secret.txt', which reported 0 bytes in size, hides some binary content. I couldn't immediately find the way to extract that in powershell and finally used a [tool](https://www.nirsoft.net/utils/alternate_data_streams.html) to do that.

Running strings on the .exe reveals the flag `cd22{REDACTED}`

Many people solved this challenge, it was a really simple one.
