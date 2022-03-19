# Snek

After pretty printing the source code, we can immediatly see that we are facing a Google Firebase challenge:

```javascript
const firebaseConfig = {
    'apiKey': _0x1110a9(0x186),
    'authDomain': _0x1110a9(0x1bd),
    'projectId': _0x1110a9(0x19d),
    'storageBucket': 'snek-56e7b.appspot.com',
    'messagingSenderId': '733133254301',
    'appId': '1:733133254301:web:5b3d458640173c67f12e74',
    'measurementId': _0x1110a9(0x197)
};
firebase['initializeApp'](firebaseConfig),
db = firebase[_0x1110a9(0x1a8)]();
```

There is some obfuscation going on here. `_0x1110a9(0x1a8)` just returns 'firestore', so the last line translates to:

```javascript
db = firebase.firestore();
```

Looking around some more we run into a function called `find_highscore`:
            
```javascript
async function find_highscore() {
    const _0x328fc9 = _0x1110a9
        , _0x48337b = [];
    top_ = await db['collection'](_0x328fc9(0x19c))[_0x328fc9(0x1aa)](_0x328fc9(0x1bc), _0x328fc9(0x185))[_0x328fc9(0x193)](),
    top_['forEach'](_0x204c3c=>_0x48337b[_0x328fc9(0x1b2)]({
        'id': _0x204c3c['id'],
        ..._0x204c3c[_0x328fc9(0x1b1)]()
    })),
    document.[_0x328fc9(0x1b8)](_0x328fc9(0x187))[_0x328fc9(0x189)] = _0x48337b[0x0]['score'] + _0x328fc9(0x1b0) + _0x48337b[0x0]['name'],
    highscore = _0x48337b[0x0][_0x328fc9(0x1bc)];
}
```

After unobfuscation it looks more like this:

```javascript
async function find_highscore() {
    const res = [];

    rows = await db.collection('scoreboard').orderBy('score','desc').get();
    rows.forEach(row => res.push({
        'id': row.id,
        ...row.data()
    }));

    document.getElementById('highscore').innerText = res[0].score + ' - ' + res[0].name;
    highscore = res[0].score;
}
```

OK, there is a `scoreboard` collection. Let's try to dump it. Paste this into the developer console:

```javascript
res = [];
db.collection('scoreboard').get()
    .then(rows => rows.forEach(row => res.push(row.data())))
    .then(() => console.log(JSON.stringify(res, undefined, 4)));
```

I know it's ugly. But, a bunch of data shows up:

```JSON
[
    {
        "score": 10,
        "name": "fgsd"
    },
    {
        "score": "infinity+6",
        "name": "orangejuice"
    },
    {
        "name": "{\"score\":\"2000\"}",
        "score": 0
    },
    {
    ...
```

We just need to grep for `cd22{` to get the flag REDACTED. There are a few false positives because our fellow competitiors added fake flags during the contest.
