/*
 * Tests functions for square matrices.
 * CSC 225, Assignment 7
 * Given tests, Winter '24
 */

#include <assert.h>
#include <stdio.h>
#include "matrix.h"

/* test01matscl: Tests multidimensional matrix scaling. */
void test01matscl(void) {
    int mat[2][2] = {{1, 2}, {3, 4}};

    matscl(&mat[0][0], 2, 2);

    assert(mat[0][0] == 2);
    assert(mat[0][1] == 4);
    assert(mat[1][0] == 6);
    assert(mat[1][1] == 8);
}

/* My test for testing scalar multiplication of a 3x3 matrix */
void test_my_matscl(void) {
    int mat[3][3] = {{1, 2, 4}, {3, 4, 5}, {10, 20, 30}};

    matscl(&mat[0][0], 3, 2);
    
    assert(mat[0][0] == 2);
    assert(mat[0][1] == 4);
    assert(mat[0][2] == 8);

    assert(mat[1][0] == 6);
    assert(mat[1][1] == 8);
    assert(mat[1][2] == 10);

    assert(mat[2][0] == 20);
    assert(mat[2][1] == 40);
    assert(mat[2][2] == 60);
    

}

/* test02matpscl: Tests array-of-pointers matrix scaling. */
void test02matpscl(void) {
    int row1[2] = {1, 2}, row2[2] = {3, 4}, *mat[2];

    mat[0] = row1;
    mat[1] = row2;
    matpscl(mat, 2, 2);

    assert(mat[0][0] == 2);
    assert(mat[0][1] == 4);
    assert(mat[1][0] == 6);
    assert(mat[1][1] == 8);
}

/* test03mattrn: Tests multidimensional matrix transposition. */
void test03mattrn(void) {
    int mat[2][2] = {{1, 2}, {3, 4}};

    mattrn(&mat[0][0], 2);
    
    assert(mat[0][0] == 1);
    assert(mat[0][1] == 3);
    assert(mat[1][0] == 2);
    assert(mat[1][1] == 4);
    
}
/*
1 4 7
2 5 8
3 6 9
*/
/* My test for testing scalar multiplication of a 3x3 matrix */
void test_my_mattrn(void) {
    int mat[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};

    mattrn(&mat[0][0], 3);
    
    assert(mat[0][0] == 1);
    assert(mat[0][1] == 4);
    assert(mat[0][2] == 7);

    assert(mat[1][0] == 2);
    assert(mat[1][1] == 5);
    assert(mat[1][2] == 8);

    assert(mat[2][0] == 3);
    assert(mat[2][1] == 6);
    assert(mat[2][2] == 9);
    

}

/* test04matptrn: Tests array-of-pointers matrix scaling. */
void test04matptrn(void) {
    int row1[2] = {1, 2}, row2[2] = {3, 4}, *mat[2];

    mat[0] = row1;
    mat[1] = row2;
    matptrn(mat, 2);

    assert(mat[0][0] == 1);
    assert(mat[0][1] == 3);
    assert(mat[1][0] == 2);
    assert(mat[1][1] == 4);
}

/* test05matadd: Tests multidimensional matrix addition. */
void test05matadd(void) {
    int mata[2][2] = {{1, 2}, {3, 4}},
        matb[2][2] = {{4, 3}, {2, 1}},
        matc[2][2];

    matadd(&mata[0][0], &matb[0][0], &matc[0][0], 2);

    assert(matc[0][0] == 5);
    assert(matc[0][1] == 5);
    assert(matc[1][0] == 5);
    assert(matc[1][1] == 5);
}

/* test06matpadd: Tests array-of-pointers matrix addition. */
void test06matpadd(void) {
    int row1[2] = {1, 2}, row2[2] = {3, 4}, *mata[2],
        row3[2] = {4, 3}, row4[2] = {2, 1}, *matb[2],
        row5[2], row6[2], *matc[2];

    mata[0] = row1;
    mata[1] = row2;
    matb[0] = row3;
    matb[1] = row4;
    matc[0] = row5;
    matc[1] = row6;
    matpadd(mata, matb, matc, 2);

    assert(matc[0][0] == 5);
    assert(matc[0][1] == 5);
    assert(matc[1][0] == 5);
    assert(matc[1][1] == 5);
}

/* test07matmul: Tests multidimensional matrix multiplication. */
void test07matmul(void) {
    int mata[2][2] = {{1, 2}, {3, 4}},
        matb[2][2] = {{4, 3}, {2, 1}},
        matc[2][2];

    matmul(&mata[0][0], &matb[0][0], &matc[0][0], 2);

    assert(matc[0][0] == 8);
    assert(matc[0][1] == 5);
    assert(matc[1][0] == 20);
    assert(matc[1][1] == 13);
}

void test_my_matmul(void) {
    int mata[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}},
        matb[3][3] = {{10, 10, 10}, {1, 1, 1}, {0, 0, 0}},
        matc[3][3];

    matmul(&mata[0][0], &matb[0][0], &matc[0][0], 3);

    /*
    printf("%d ", matc[0][0]);
    printf("%d ", matc[0][1]);
    printf("%d \n", matc[0][2]);
    printf("%d ", matc[1][0]);
    printf("%d ", matc[1][1]);
    printf("%d ", matc[1][2]);
    */
    
    assert(matc[0][0] == 12);
    assert(matc[0][1] == 12);
    assert(matc[0][2] == 12);
     
    assert(matc[1][0] == 45);
    assert(matc[1][1] == 45);
    assert(matc[1][2] == 45);

    assert(matc[2][0] == 78);
    assert(matc[2][1] == 78);
    assert(matc[2][2] == 78);
    
}

/* test08matpmul: Tests array-of-pointers matrix multiplication. */
void test08matpmul(void) {
    int row1[2] = {1, 2}, row2[2] = {3, 4}, *mata[2],
        row3[2] = {4, 3}, row4[2] = {2, 1}, *matb[2],
        row5[2], row6[2], *matc[2];

    mata[0] = row1;
    mata[1] = row2;
    matb[0] = row3;
    matb[1] = row4;
    matc[0] = row5;
    matc[1] = row6;
    matpmul(mata, matb, matc, 2);

    assert(matc[0][0] == 8);
    assert(matc[0][1] == 5);
    assert(matc[1][0] == 20);
    assert(matc[1][1] == 13);
}

void test_mymatpmul(void) {
    int rowA1[3] = {1, 2, 3}, rowA2[3] = {4, 5, 6}, rowA3[3] = {7, 8, 9}, *mata[3],
        rowB1[3] = {10, 10, 10}, rowB2[3] = {1, 1, 1}, rowB3[3] = {0, 0, 0}, *matb[3],
        rowC1[3], rowC2[3], rowC3[3], *matc[3];

    mata[0] = rowA1;
    mata[1] = rowA2;
    mata[2] = rowA3;

    matb[0] = rowB1;
    matb[1] = rowB2;
    matb[2] = rowB3;

    matc[0] = rowC1;
    matc[1] = rowC2;
    matc[2] = rowC3;

    matpmul(mata, matb, matc, 3);
    /*
    printf("%d ", matc[0][0]);
    printf("%d ", matc[0][1]);
    printf("%d \n", matc[0][2]);
    printf("%d ", matc[1][0]);
    printf("%d ", matc[1][1]);
    printf("%d ", matc[1][2]);
    */
    assert(matc[0][0] == 12);
    
    assert(matc[0][1] == 12);
    assert(matc[0][2] == 12);
     
    assert(matc[1][0] == 45);
    assert(matc[1][1] == 45);
    assert(matc[1][2] == 45);

    assert(matc[2][0] == 78);
    assert(matc[2][1] == 78);
    assert(matc[2][2] == 78);
    
}

int main(void) {
    /* Scalar tests */
    test01matscl();
    test_my_matscl();
    
    test02matpscl();
    

    /* Transposition tests */
    test03mattrn();
    test_my_mattrn();

    test04matptrn();
    
    /* Matrix Addition */
    test05matadd();
    
    test06matpadd();
    
    /* Matrix Mulitplication */
    test07matmul();
    test_my_matmul();

    test08matpmul(); 
    test_mymatpmul();
    
    return 0;
}
