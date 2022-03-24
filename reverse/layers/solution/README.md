# Layers

This is a simple challenge, solveable with `gdb`. Let's start the binary in a Linux machine:

```shell
> ./layers
Okay, um, Ogres are like onions.
```

It's waiting for some input. If you enter something it just terminates:
```shell
> ./layers
Okay, um, Ogres are like onions.
hello
Wrong!
```

Start it in a debugger.
```shell
> gdb ./layers
{... lots of stuff ...}
(gdb) r
Starting program: /media/psf/Home/projects/secchallenge2022/reverse/layers/input/layers 
Okay, um, Ogres are like onions.
```
Hit Ctrl+C: 
```
^C
Program received signal SIGINT, Interrupt.
0x00007ffff7263360 in __read_nocancel () at ../sysdeps/unix/syscall-template.S:84
84	../sysdeps/unix/syscall-template.S: No such file or directory.
(gdb) bt
#0  0x00007ffff7263360 in __read_nocancel () at ../sysdeps/unix/syscall-template.S:84
#1  0x00007ffff71e65f8 in _IO_new_file_underflow (fp=0x7ffff75308e0 <_IO_2_1_stdin_>) at fileops.c:592
#2  0x00007ffff71e761e in __GI__IO_default_uflow (fp=0x7ffff75308e0 <_IO_2_1_stdin_>) at genops.c:413
#3  0x00007ffff71dac7a in __GI__IO_getline_info (fp=fp@entry=0x7ffff75308e0 <_IO_2_1_stdin_>, buf=buf@entry=0x7fffffffda70 "", 
    n=31, delim=delim@entry=10, extract_delim=extract_delim@entry=1, eof=eof@entry=0x0) at iogetline.c:60
#4  0x00007ffff71dad88 in __GI__IO_getline (fp=fp@entry=0x7ffff75308e0 <_IO_2_1_stdin_>, buf=buf@entry=0x7fffffffda70 "", 
    n=<optimized out>, delim=delim@entry=10, extract_delim=extract_delim@entry=1) at iogetline.c:34
#5  0x00007ffff71d9b8d in _IO_fgets (buf=0x7fffffffda70 "", n=<optimized out>, fp=0x7ffff75308e0 <_IO_2_1_stdin_>) at iofgets.c:53
#6  0x000000000040162f in ?? ()
#7  0x00007ffff718c840 in __libc_start_main (main=0x401540, argc=1, argv=0x7fffffffdb88, init=<optimized out>, 
    fini=<optimized out>, rtld_fini=<optimized out>, stack_end=0x7fffffffdb78) at ../csu/libc-start.c:291
#8  0x000000000040111e in ?? ()

```

It's in the middle of an fgets call. Put a breakpoint to `0x40162f`, this is where it returns from that.

```shell
(gdb) b *0x40162f
Breakpoint 1 at 0x40162f
(gdb) c
Continuing.
alma

Breakpoint 1, 0x000000000040162f in ?? ()
(gdb)
```

Switch to asm view:
```shell
(gdb) layout asm
   ┌─────────────────────────────────────────────────────────────────────────┐
B+>│0x40162f        movabs $0x6c627777787f426a,%rax                          │
   │0x401639        movabs $0x6562316874794531,%rdx                          │
   │0x401643        mov    %rax,0x11(%rsp)                                   │
   │0x401648        mov    %rdx,0x19(%rsp)                                   │
   │0x40164d        movl   $0x2e7a7f78,0x21(%rsp)                            │
   │0x401655        movw   $0x1b,0x25(%rsp)                                  │
   │0x40165c        movb   $0x0,0x27(%rsp)                                   │
   │0x401661        lea    0x11(%rsp),%rax                                   │
   │0x401666        lea    0x26(%rsp),%rdx                                   │
   │0x40166b        xorb   $0x11,(%rax)                                      │
   │0x40166e        add    $0x1,%rax                                         │
   │0x401672        cmp    %rdx,%rax                                         │
   │0x401675        jne    0x40166b                                          │
   │0x401677        movb   $0x0,0x26(%rsp)                                   │
   │0x40167c        movb   $0x1,0x27(%rsp)                                   │
   │0x401681        lea    0x11(%rsp),%rsi                                   │
   │0x401686        lea    0x40(%rsp),%rdi                                   │
   │0x40168b        callq  0x4010c0 <strcmp@plt>                             │
   │0x401690        test   %eax,%eax                                         │
   │0x401692        jne    0x4016ae                                          │
   │0x401694        callq  0x40215d                                          │
   │0x401699        mov    0x68(%rsp),%rdx                                   │
   │0x40169e        sub    %fs:0x28,%rdx                                     │
   │0x4016a7        jne    0x401726                                          │
   └─────────────────────────────────────────────────────────────────────────┘
native process 9019 In:                                    L??   PC: 0x40162f 
(gdb) 
```
It seams that it's doing some decryption then compares our input to the result. We are interested in `0x40168b callq  0x4010c0 <strcmp@plt>`
```shell
(gdb) b *0x40168b
Breakpoint 2 at 0x40168b
(gdb) c
Continuing.

Breakpoint 2, 0x000000000040168b in ?? ()
```
Let's see what it compares:
```shell
(gdb) x/s $rdi
0x7fffffffda70: "alma\n"
(gdb) x/s $rsi
0x7fffffffda41: "{Sniffs} They stink?\n"
(gdb) 
```
So we have the string we entered and the expected one. If we give it the right answer the dialog continues. Or we can put a breakpoint to `0x401690` as well and set the return value in `$rax` to `0`, so that the program thinks we are on track.

```shell
(gdb) set $rax = 0
```

This way or other the process can be repeated a couple of times to unfold the story with the flag:

```shell
Okay, um, Ogres are like onions.
{Sniffs} They stink?  
Yes... No!
They make you cry?
No! Layers! Onions have layers. Ogres have layers! Onions have layers. You get it? We both have layers.
Oh, you both have layers. You know, not everybody likes onions.
You dense, irritating, miniature beast of burden, Ogres are like onions!
Parfaits may be the most delicious thing on the whole damn planet.
You know what is something everybody likes?
REDACTED
REDACTED
```

![](shrek.jpg)
