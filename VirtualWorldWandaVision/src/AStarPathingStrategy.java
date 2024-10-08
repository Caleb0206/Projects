import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.function.BiPredicate;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Stream;

public class AStarPathingStrategy implements PathingStrategy {

    /**
     * Return a list containing a single point representing the next step toward a goal
     * If the start is within reach of the goal, the returned list is empty.
     *
     * @param start the point to begin the search from
     * @param end the point to search for a point within reach of
     * @param canPassThrough a function that returns true if the given point is traversable
     * @param withinReach a function that returns true if both points are within reach of each other
     * @param potentialNeighbors a function that returns the neighbors of a given point, as a stream
     */
    public List<Point> computePath(
            Point start,
            Point end,
            Predicate<Point> canPassThrough,
            BiPredicate<Point, Point> withinReach,
            Function<Point, Stream<Point>> potentialNeighbors
    ) {
        // If already within reach of the goal, return an empty list
        if (withinReach.test(start, end)) {
            return new ArrayList<>();
        }
        Node initial = new Node(start.x, start.y, 0, getHScore(start, end), getHScore(start, end), null);

        // create data structures to hold Nodes and other values
        List<Node> openSet = new ArrayList<>();
        List<Node> closedSet = new ArrayList<>();

        // add the start point (as Node initial)
        openSet.add(initial);

        boolean finished = false;   // this boolean tells the loop if the path is complete or not
        while(!openSet.isEmpty() && !finished) {
            openSet.sort(Comparator.comparing(node -> node.fScore));    // sort openSet by fScore
            Node current = openSet.get(0);                              // gets the node with the least f-score

            if(withinReach.test(current, end)) {
                // stop loop if within reach of goal
                finished = true;
            }
            else {
                // get neighbors providing its specific qualities within bounds and other possible stuff
                List<Point> neighbors = potentialNeighbors.apply(current)
                        .filter(canPassThrough)
                        .toList();


                // remove current node from openSet
                openSet.remove(current);

                // add current node to closed set
                closedSet.add(current);

                // go through list of neighbors
                for (Point tempPoint : neighbors) {
                    // create a Node for neighboring position:
                    int tempG = current.gScore + 1;
                    int tempH = getHScore(tempPoint, end);
                    int tempF = tempG + tempH;
                    Node tempNode = new Node(tempPoint.x, tempPoint.y, tempG, tempH, tempF, current);

                    if (!closedSet.contains(tempNode) && !openSet.contains(tempNode)) {
                        openSet.add(tempNode);      // only adds new node values
                    } else if (!closedSet.contains(tempNode) && openSet.contains(tempNode)) {
                        // the neighbor is in open set and the current gScore is greater than this new Node, override its values

                        for (Node nde : openSet) {
                            if (nde.x == tempNode.x && nde.y == tempNode.y && nde.gScore > tempNode.gScore) {
                                nde.gScore = tempNode.gScore;
                                nde.hScore = tempNode.hScore;
                                nde.fScore = tempNode.fScore;
                                nde.prevNode = tempNode.prevNode;
                                break;
                            }
                        }
                    }
                }
            }
        }
        List<Point> thePath = new ArrayList<>();

        if (openSet.isEmpty())  // the target is right next to it
            return new ArrayList<>();
        Node tempPathNode = openSet.get(0);
        while (tempPathNode.prevNode != null) {
            thePath.add(tempPathNode);
            tempPathNode = tempPathNode.prevNode;
        }
        thePath.remove(initial);
        if (thePath.isEmpty())
            return new ArrayList<>();

        Collections.reverse(thePath); // reverses the list (from GeeksForGeeks)
        return thePath;
    }
    public int getHScore(Point begin, Point end) {
        return Math.abs(begin.x - end.x) + Math.abs(begin.y - end.y);
    }


}
