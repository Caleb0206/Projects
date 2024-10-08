/**
 * A partial 'Node' class. Modify as necessary.
 *
 * @author Vanessa Rivera
 * @author Caleb Huang
 */
class BigNumberNode {
    private int data;
    private BigNumberNode next;

    public BigNumberNode(int data) {
        this.data = data;
        this.next = null;
    }
    public void setNext(BigNumberNode nxt) {
        next = nxt;
    }
    public BigNumberNode getNext() {
        return next;
    }
    public int getData() {
        return data;
    }
}