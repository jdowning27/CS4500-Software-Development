# anton
CS 4500 Project Repo by Jennifer Der and Timothy Haas

## B — Command Line
Command line program `xyes` that will print according to given arguments. Related files in directory `B/`

**Example Usage**
```
$ ./xyes [-limit] [arg1 arg2 ...argN]
```
Which will print the concatenated command line arguments `[arg1 arg2 ...argN]` separated by a single ASCII blank space an inifinite number of times. If `-limit` is supplied, the program will only print 20 times. If there are no command line arguments to form the output string, the program uses `"hello world"` instead.

For example `$ ./xyes -limit a b c` will print the string "a b c" 20 times in the console.

**How to run tests**
```
# from the B/Other directory
sh test_xyes.sh
```