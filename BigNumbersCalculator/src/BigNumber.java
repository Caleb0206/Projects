import javax.swing.*;

/**
 * A partial linked list class. Modify as necessary.
 *
 * @author Vanessa Rivera
 * @author Caleb Huang
 */
public class BigNumber {

    private BigNumberNode head;

    public BigNumber() {
        head = null;
    }
    public BigNumber(BigNumberNode node) {
        head = node;
    }
    // TODO: Write addition, multiplication, and exponentiation methods here or in another class
    public BigNumber add(BigNumber addend) {
        BigNumberNode thisCurrent = head;
        BigNumberNode addendCurrent = addend.head;

        BigNumber sum = new BigNumber();
        BigNumberNode sumCurrent = null;
        int carry = 0;
        while (thisCurrent != null && addendCurrent != null) {
            BigNumberNode temp;
            int a = thisCurrent.getData();
            int b = addendCurrent.getData();
            if (a + b + carry >= 10) {
                int diff = a + b + carry - 10;
                temp = new BigNumberNode(diff);
                carry = 1;
            } else {
                temp = new BigNumberNode(a + b + carry);
                carry = 0;
            }

            if (sumCurrent == null) {
                sum.head = temp;
                sumCurrent = sum.head;
            }
            else {
                sumCurrent.setNext(temp);
                sumCurrent = sumCurrent.getNext();
            }
            // Increment the current nodes of this BigNumber and the param's current node
            thisCurrent = thisCurrent.getNext();
            addendCurrent = addendCurrent.getNext();
        }

        // If the addend is longer than this Big Number
        if (thisCurrent == null && addendCurrent != null) {
            while (addendCurrent != null) {
                // Check for carry
                if (carry == 0) {
                    sumCurrent.setNext(addendCurrent);
                }
                else {
                    if (addendCurrent.getData() + carry < 10 ) {
                        BigNumberNode tempCarried = new BigNumberNode(addendCurrent.getData() + carry);
                        sumCurrent.setNext(tempCarried);
                        carry = 0;
                    }
                    else {
                        BigNumberNode tempCarried = new BigNumberNode(addendCurrent.getData() + carry - 10);
                        sumCurrent.setNext(tempCarried);
                        carry = 1;
                    }

                }
                sumCurrent = sumCurrent.getNext();
                addendCurrent = addendCurrent.getNext();
            }
        } else if (addendCurrent == null && thisCurrent != null) {      // If this BigNumber is longer than the addend
            while (thisCurrent != null) {
                if (carry == 0) {
                    sumCurrent.setNext(thisCurrent);
                }
                else {
                    if (thisCurrent.getData() + carry < 10 ) {
                        BigNumberNode tempCarried = new BigNumberNode(thisCurrent.getData() + carry);
                        sumCurrent.setNext(tempCarried);
                        carry = 0;
                    }
                    else {
                        BigNumberNode tempCarried = new BigNumberNode(thisCurrent.getData() + carry - 10);
                        sumCurrent.setNext(tempCarried);
                        carry = 1;
                    }
                }

                sumCurrent = sumCurrent.getNext();
                thisCurrent = thisCurrent.getNext();
            }
        }

        // final check for if carry is still 1
        if (carry == 1) {
            BigNumberNode carryOne = new BigNumberNode(1);
            sumCurrent.setNext(carryOne);
        }

        return sum;
    }

    public BigNumber multiply(BigNumber second) {
        BigNumberNode thisCurrent = head;
        BigNumber product = new BigNumber();
        int numPosition = 0;

        while (thisCurrent != null) {
            int a = thisCurrent.getData();
            int carry = 0;
            BigNumberNode secondCurrent = second.head;
            BigNumberNode productCurrent = null;
            BigNumber tempProduct = new BigNumber();
            BigNumberNode result = null;

            while (secondCurrent != null) {
                int b = secondCurrent.getData();
                int tempResult = a * b + carry;

                if(productCurrent == null) {
                    productCurrent = new BigNumberNode(tempResult % 10);
                    if (numPosition == 0)
                        product.head = productCurrent;
                    tempProduct.head = productCurrent;
                }
                else {
                    while (productCurrent.getNext() != null) {
                        productCurrent = productCurrent.getNext();
                    }
                    productCurrent.setNext(new BigNumberNode(tempResult % 10));
                }
                carry = tempResult / 10;
                secondCurrent = secondCurrent.getNext();
            }
            if (carry > 0 ) {
                while (productCurrent.getNext() != null) {
                    productCurrent = productCurrent.getNext();
                }
                productCurrent.setNext(new BigNumberNode(carry));

            }
            for (int i = 0; i < numPosition; i++) {
                result = new BigNumberNode(0);
                result.setNext(tempProduct.head);
                tempProduct.head = result;
            }
            numPosition++;
            if (result != null) {
                product = product.add(tempProduct);
            }
            thisCurrent = thisCurrent.getNext();
        }

        return  product;
    }

    public BigNumber exponentiate(int exponent) {
        BigNumber result = new BigNumber();
        BigNumber initial = new BigNumber();
        if (exponent == 0)
            result.head = new BigNumberNode(1);
        else if (exponent % 2 == 0) {
            // even exponent
            BigNumber copy = new BigNumber(this.head);
            initial = multiply(copy);
            result = initial;
            exponent = exponent / 2;
            for (int i = 1; i < exponent; i++) {
                result = result.multiply(initial);
            }

        }
        else {
            // odd exponent
            BigNumber copy = new BigNumber(this.head);
            initial = multiply(copy);
            result.head = initial.head;
            exponent = (exponent - 1) / 2;
            for (int i = 1; i < exponent; i++) {
                result = initial.multiply(initial);
            }
            result = result.multiply(copy);
        }
        return result;
    }
    public static BigNumber fromString(String string) {
        // TODO: Use the string to create your BigNumber here (Hint: use iteration or recursion)
        BigNumber num = new BigNumber();
        if (string == null || string.isEmpty())
            return num;

        BigNumberNode current = null;

        for (int i = string.length() - 1; i >= 0; i--) {
            BigNumberNode temp = new BigNumberNode(Integer.parseInt("" + string.charAt(i)) );
            if (current == null) {
                num.head = temp;
                current = temp;
            }
            else {
                current.setNext(temp);
                current = temp;
            }
        }

        return num;
    }

    @Override
    public String toString() {
        String string = "";

        // TODO: Create your string using the BigNumber here (Hint: use iteration or recursion)
        BigNumberNode current = head;
        while (current != null) {
            string = current.getData() + string;
            current = current.getNext();
        }
        return string;
    }
}
