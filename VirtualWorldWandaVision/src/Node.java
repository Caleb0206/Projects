public class Node extends Point{

    public int gScore, hScore, fScore;
    public Node prevNode;
    public Node(int x, int y, int g, int h, int f, Node previous) {
        super(x, y);
        gScore = g;
        hScore = h;
        fScore = f;
        prevNode = previous;
    }





}
