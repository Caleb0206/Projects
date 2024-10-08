#include <stdio.h>
#include "fib.h"
/*
 * Recursively computes Fibonacci numbers.
 * CSC 225, Assignment 6
 * Given code, Winter '24.
 * TODO: Complete this file.
 */

int main(void) {
    int input, result;
    printf("Enter an integer: ");
    scanf("%d", &input);
    result = fib(input);
    printf("f(%d) = %d", input, result);
    printf("\n");
    return result;
}
