/*
 * Defines functions for computing Fibonacci numbers.
 * CSC 225, Assignment 6
 * Given code, Winter '24.
 * NOTE: Do not alter this file.
 */

/* fib: Computes the "n"th Fibonacci number. */
int fib(int n) {
    int a, b;

    if (n <= 0) {
        return 0;
    }
    else if (n == 1) {
        return 1;
    }
    else {
        a = fib(n - 1); 
        b = fib(n - 2); 
        return a + b;
    }
}
