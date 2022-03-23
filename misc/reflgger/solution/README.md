# refl🤣gger

Reflogger was a forensics challenge. You find a git repository with 100 files numbered from 00 to 99 in the provided `.tar`.

The git history is not very talkative:

```shell
> git log
commit ff4e4e30d01e1d6459662a949ee02d13f583e371
Author: kergemarha <kergemarha@k.or>
Date:   Mon Jan 24 20:23:06 2022 +0100

    ewHDOXQUKq

commit 2c579050b765cb9ee6a679309a68bc11c52bc8a3
Author: kergemarha <kergemarha@k.or>
Date:   Mon Jan 24 20:23:05 2022 +0100

    AglEAtgiey

commit 798f5b768bc39edd1fdf61669de561c9c01b9fd1
Author: kergemarha <kergemarha@k.or>
Date:   Mon Jan 24 20:23:05 2022 +0100

    MwSIVUeDWB
...
```

The changes also look pretty random:
```shell
> git diff HEAD~1
diff --git a/02 b/02
index c4e9d5e..148b8ba 100644
--- a/02
+++ b/02
@@ -1 +1,2 @@
 KVkkDezSGQwTNHrPgKoEzeooWtVrbpQqRIkZoowdstRQdmtSuGsAeFQPBWQmSHRLNSbYTucHOSofpjGnwPiGDLPXCAgGwZTJBNmv
+ujvWOzlpcUeXzbtTaaLFTlFjkZJdYgnhULqjsmiKqihFJDJmCMlUamXtwcLcTlSrkleRRPhimWvSuUglTUIsNXaPHbZFPbSPutSa
diff --git a/67 b/67
index 42d2655..805e965 100644
--- a/67
+++ b/67
@@ -1 +1 @@
-LKaiWAnDOBiAdCklgXCkWnBErPEqbJZNLCFyFMEbIRieYknfJxAnoHvqPghghibSBhshKgrZLTOZaQERGcZESkIVxGOllipttUxi
+TDKkAzdXWUtGjXlqiBUHLozooRkDqFxfAGbcgHJytvbTBcOxJZHEVeTanWoVRtveQawJrqAQgbPQwzpBKgemPniCqDknUwRDtmQk
```

Reflog says there was a bunch of reset in the history:
```shell
> git reflog | head
ff4e4e3 HEAD@{0}: commit: ewHDOXQUKq
2c57905 HEAD@{1}: reset: moving to HEAD~1
86a3e66 HEAD@{2}: commit: ehFvDTjFkQ
2c57905 HEAD@{3}: reset: moving to HEAD~2
ab5af75 HEAD@{4}: commit: vmdWukgtSk
d7534a5 HEAD@{5}: commit: ZFstCsjfil
2c57905 HEAD@{6}: reset: moving to HEAD~1
c0e8d1e HEAD@{7}: commit: wSGdXfPMTj
2c57905 HEAD@{8}: commit: AglEAtgiey
798f5b7 HEAD@{9}: reset: moving to HEAD~4
```

One trick we can pull off is listing all objects the repo knows about:

```shell
> git cat-file --batch-check --batch-all-objects --unordered | head
00ce77f9c573a97ac283ba38f02a41c568bea2bd tree 3000
00ffeff5aba633359e605ab0f8587fae00dcd1da commit 215
008ed4d607243764565957f6d611951310027fc2 tree 3000
000f51932d4d06c85ba6747393963ee57c79b83e blob 101
00b1e6b268851ad91b5eab4f6f170e21dbd35c45 blob 101
00d77d12177306787f6ad9193aa2d9f3e0463506 tree 840
00494516dbf704bdc818795ac73ac7181cc75f94 commit 215
007ef54ce0ec7041525c824a7fa4fa9141c232b3 blob 101
00aa33a69c919dfe9626c12e567ca68073c34645 blob 202
00ea64e5682680807c94e05bd4c816ace30a8727 commit 215
```

We are getting somewhere. We need the blobs only:
```shell
> git cat-file --batch-check --batch-all-objects --unordered | grep blob | head
000f51932d4d06c85ba6747393963ee57c79b83e blob 101
00b1e6b268851ad91b5eab4f6f170e21dbd35c45 blob 101
007ef54ce0ec7041525c824a7fa4fa9141c232b3 blob 101
00aa33a69c919dfe9626c12e567ca68073c34645 blob 202
0185029f379db1d55066a4d07bc6c1fb2068605d blob 101
01a02940f44f242b2f9040ec33d405597f7e7bfb blob 101
01010ec81a9711d8f6600fef967cae992ce7ffef blob 101
02f9d1a27e2301ad398a8bdd39b52d0983405633 blob 101
02397c8ee2dfc61c7d74054a8a51ab65d88bdf32 blob 101
020746d435de8d872944aae90d9e6e0e95545e77 blob 101
```

The command `git cat-file` can retrieve such a blob:

```shell
> git cat-file -p 020746d435de8d872944aae90d9e6e0e95545e77
bnGPfZHIiacSDLaEzpeNupkpJwfrpEfPBMMAhldoHofYylafIwDvrnGZlIrFYBnRVkWZQlxGmqzxYdsQvjfbeBtfGsgrHWpWNqZu
```

We better fetch all of them into a single file:
```shell
> git cat-file --batch-check --batch-all-objects --unordered | grep blob | awk -F " " '{print($1)}' > blobs
> for f in $(cat blobs); do git cat-file -p $f; done > content
```

Now we have everything the repository tracks, added or removed. Let's sort it by length:
```shell
> cat content | awk '{ print length, $0 }' | sort -n -s | cut -d" " -f2-
...
    j = 0
import os
    x = ""
    x = ""
def drop():
    ssssss(
def reset():
def squash():
import random
import string
HLENGTH = 100
import string
def ssssss(s):
        j += 1
def randfname():
os.chdir("wdir")
    os.system(s)
ssssss("git init")
    print(">>> "+s)
    git(HLENGTH, F)
def commit_append():
from flag import FLAG
ssssss("rm -rf wdir")
from sys import stderr
    while len(x) < 50:
ssssss("mkdir -p wdir")
def commit_overwrite():
def randstring(length):
    ssssss("git add .")
    for i in range(100):
    for i in range(1000):
            x = ff.read()
if __name__ == "__main__":
        commit_overwrite()
        ssssss("git add .")
        with open(f) as ff:
        stderr.writelines(i)
def git(iterations, functions):
    for i in range(iterations):
def git(iterations, functions):
    pos = random.randrange(2, 5)
        random.choice(functions)()
        f = random.choice(os.listdir())
        # ssssss(f"git commit -m code{j}")
    for i in open("../gen.py").readlines():
    ssssss(f"git commit -m {randstring(10)}")
        ssssss(f"git commit -m {randstring(10)}")
        ssssss(f"git commit -m {randstring(10)}")
F = [commit_append, commit_overwrite, reset, squash]
    ssssss(f"echo {randstring(100)} > {randfname()}")
    return "".join(random.choices(string.digits, k=2))
    ssssss(f"echo {randstring(100)} >> {randfname()}")
IDk2LCA4NSwgMTA4LCAxMTAsIDM3LCAxMTQsIDMyLCA1LCAyLCAxMF0K
IDk2LCA4NSwgMTA4LCAxMTAsIDM3LCAxMTQsIDMyLCA1LCAyLCAxMF0K
    ssssss(f"git reset --hard HEAD~{random.randrange(1,5)}")
    ssssss(f"git reset --soft HEAD~{random.randrange(1,5)}")
    return "".join(random.choices(string.ascii_letters, k=length))
    ssssss(f"git rebase --onto master~{pos} master~{pos-1} master~{pos-2}")
        f"echo {[ord(i) ^ ord(y) for i,y in zip(FLAG,x)]} | base64 - > {f}")
...
...
...
lots of garbage here
...
...
...
# 🤣🤣😂🤣😂😂😂🤣😂＼（〇_ｏ）／(＃°Д°)...(*￣０￣)ノ(⊙o⊙)(⊙_(⊙_⊙)_⊙)👀🥙🥩🍗🍖🙄😌😴
```

We get lots of random looking strings having the same length (not shown above), plus some Python code fragments. I played with it for a while and figured out that the lines are
probably part of the Python script that was used to generate the repo. It's randomly doing
various things, sometimes taking a line of its own source and commiting it in a file. It has
operations to drop a few commits, generate some garbage etc, and it uses randomized commit
messages.

One interesting part is:

```python
from flag import FLAG
    ...
    while len(x) < 50:
        f = random.choice(os.listdir())
        with open(f) as ff:
            x = ff.read()
    ssssss(
        f"echo {[ord(i) ^ ord(y) for i,y in zip(FLAG,x)]} | base64 - > {f}")
    ...
```

I came up with this just playing jigsaw puzzle with the lines above. The indentation helps a lot. What it seems to be doing is taking files randomly, reading the contents until it finds a long enough one. Then takes whatever is in the FLAG variable and xors the file's content with it. Runs base64 on the result and probably overwrites the orginial file with it...

Here is the plan: make pairs of the garbage lines base64 decode one of them 
and xor it with the other one. If the result contains `cd22` we are done.

At least that's what I was thinking, but nothing came out of it... I thought I was missing some lines because didn't extract everything from the repository, but the answer was more surprising.

```python
>>> [ord(i) ^ ord(y) for i,y in zip('apple','pear')]
[17, 21, 17, 30]
```

The xor operation returns an array of numbers, and this is taken verbatim and given to the base64 encoder. It literally encodes the string `"[17, 21, 17, 30]"`. So we are not looking for `cd22` but something like `[99, 100, 50, 50....`

I modified my solver script to try to JSON parse the result of the xor operation, and decoded it as ASCII chars resulting in the flag `cd22{REDACTED}`.
