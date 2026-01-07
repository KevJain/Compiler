## Wabbit Compiler ##

This is a compiler for the Wabbit language as defined [here](https://www.dabeaz.com/wabbit.html).

Here's a sample program that computes Fibonacci numbers recursively, and the program's output:

### factre.wb
```
// Compute factorials
      
func fact(n int) int {
   if n == 0 {
      return 1;
   } else {
      return n * fact(n-1);
   }
}

var x = 1;
while x < 10 {
    print fact(x);
    x = x + 1;
}
```

### Output
```
Output: 1
Output: 2
Output: 6
Output: 24
Output: 120
Output: 720
Output: 5040
Output: 40320
Output: 362880
```

Usage: ```python compile.py [source] [executable name]```

Currently only support integers. Float and char support in progress.
