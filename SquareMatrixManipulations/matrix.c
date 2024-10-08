/*
 * Defines functions for manipulating square integer matrices.
 * CSC 225, Assignment 7
 * Given code, Winter '24
 */

#include "matrix.h"

/* matscl: Multiplies each element of a matrix by a scalar. */
void matscl(int *mat, unsigned int n, int c) {
    /* TODO: Complete this function, given:
     *  mat - A pointer to the first element in a multidimensional array
     *  n   - The height and width of the matrix
     *  c   - The constant scalar
     * ...multiply each element in "mat" by "c". */
     int i = 0, size;
     size = n * n;
     for(i = 0; i < size; i++)
     {
        *(mat + i) = *(mat + i) * c;
        /* mat[i] = mat[i] * c; */
     }
}

/* matpscl: Multiplies each element of a matrix by a scalar. */
void matpscl(int **mat, unsigned int n, int c) {
    /* TODO: Complete this function, given:
     *  mat - An array of pointers to arrays of integers
     *  n   - The height and width of the matrix
     *  c   - The constant scalar
     * ...multiply each element in "mat" by "c". */
    int row, index;

    for(row = 0; row < n; row++) 
    {
        for(index = 0; index < n; index++) 
        {
            /* mat[i] is the addresss of row 1 of the matrix, so add j to get row and column*/
            *(mat[row] + index) = *(mat[row] + index) * c;
        }
    }
}

/* mattrn: Transposes a matrix about its diagonal, in-place. */
void mattrn(int *mat, unsigned int n) {
    /* TODO: Complete this function, given:
     *  mat - A pointer to the first element in a multidimensional array
     *  n   - The height and width of the matrix
     * ...transpose "mat" about its diagonal. */
     int row, col, temp, index1, index2;

     /* 1 2 */
     /* 3 4 */

     /* 
        1  2  3  4      
        5  6  7  8 
        9  10 11 12
        13 14 15 16

        1  5  9   13
        2  6  10  14 
        3  7  11  15
        4  8  12  16
    */

    for(row = 0; row < n; row++) 
    {
        for(col = row+1; col < n; col++)    /* col should start offset 1 off of row */
        {
            index1 = row * n + col;     /* index1 = 1, index of 2 */
            index2 = col * n + row;     /* index2 = 4, index of 5 */
            temp = mat[index1];         /* store original value of index1 */
            mat[index1] = mat[index2];
            mat[index2] = temp;
        }
    }
}

/* matptrn: Transposes a matrix about its diagonal, in-place. */
void matptrn(int **mat, unsigned int n) {
    /* TODO: Complete this function, given:
     *  mat - An array of pointers to arrays of integers
     *  n   - The height and width of the matrix
     * ...transpose "mat" about its diagonal. */
    int row, index, temp;
    for(row = 0; row< n; row++) 
    {
        for(index = row+1; index < n; index++)
        {
            temp = mat[row][index];
            
            mat[row][index] = mat[index][row];
            mat[index][row] = temp;
        }
    }

}

/* matadd: Adds two matrices, placing their sum into a third. */
void matadd(int *mata, int *matb, int *matc, unsigned int n) {
    /* TODO: Complete this function, given:
     *  mata - A pointer to the first element in a multidimensional array
     *  matb - A pointer to the first element in a multidimensional array
     *  matc - A pointer to the first element in a multidimensional array
     *  n    - The height and width of the matrices
     * ...compute "matc = mata + matb". */
    int i, size;
    size = n*n;
    for(i=0; i < size; i++)
    {
        matc[i] = mata[i] + matb[i];
    }

}

/* matpadd: Adds two matrices, placing their sum into a third. */
void matpadd(int **mata, int **matb, int **matc, unsigned int n) {
    /* TODO: Complete this function, given:
     *  mata - An array of pointers to arrays of integers
     *  matb - An array of pointers to arrays of integers
     *  matc - An array of pointers to arrays of integers
     *  n    - The height and width of the matrices
     * ...compute "matc = mata + matb". */
    int row, col;
    for (row = 0; row < n; row ++)
    {
        for (col = 0; col < n; col++)
        {
            matc[row][col] = mata[row][col] + matb[row][col]; 

        }
    }
}

/* matmul: Multiplies two matrices, placing their product into a third. */
void matmul(int *mata, int *matb, int *matc, unsigned int n) {
    /* TODO: Complete this function, given:
     *  mata - A pointer to the first element in a multidimensional array
     *  matb - A pointer to the first element in a multidimensional array
     *  matc - A pointer to the first element in a multidimensional array
     *  n    - The height and width of the matrices
     * ...compute "matc = mata * matb". */
    int row, col, k;
    int tempSum = 0;
    for (row = 0; row < n; row++)
    {   
        for (col = 0; col < n; col++)
        {
            tempSum = 0;
            for (k = 0; k < n; k++) 
            {
                tempSum += mata[row*n + k] * matb[k*n + col];
            }
            matc[row * n + col] = tempSum;
        }
    }
}

/* matpmul: Multiplies two matrices, placing their product into a third. */
void matpmul(int **mata, int **matb, int **matc, unsigned int n) {
    /* TODO: Complete this function, given:
     *  mata - An array of pointers to arrays of integers
     *  matb - An array of pointers to arrays of integers
     *  matc - An array of pointers to arrays of integers
     *  n    - The height and width of the matrices
     * ...compute "matc = mata * matb". */
    int row, col, k, tempSum;
    for (row = 0; row < n; row++)
    {
        for (col = 0; col < n; col++)
        {
            tempSum = 0;
            for (k = 0; k < n; k++)
            {
                tempSum += mata[row][k] * matb[k][col];
            }
            
            matc[row][col] = tempSum;
        }
        
    }
}
