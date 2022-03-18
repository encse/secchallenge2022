This is a pretty simple level, but I ran into a couple of server side bugs which killed the
challenge for my user a couple of times. These were fixed by the organizers.

Once it was up and running I could register a new user and login.

There is a profile page where we can upload an avater either from a file or with an url. 
Since the challenge description hints that the `notekeeper` service can access the `flag` service
let's try setting the url to the nasty `http://localhost/flag`.

Take the url of the newly created avatar and download it with curl:
```
> curl https://notekeeper.secchallenge.crysys.hu/static/00000000-0000-0000-0000-000000000000/avatar
cd22{REDACTED}                                                
```

