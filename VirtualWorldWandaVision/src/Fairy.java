import processing.core.PImage;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.function.BiPredicate;
import java.util.function.Predicate;

public class Fairy extends Entity implements Moveable, Behaviorable, Animatable {
    public static final String FAIRY_KEY = "fairy";

    public static final int FAIRY_PARSE_PROPERTY_BEHAVIOR_PERIOD_INDEX = 0;
    public static final int FAIRY_PARSE_PROPERTY_ANIMATION_PERIOD_INDEX = 1;
    public static final int FAIRY_PARSE_PROPERTY_COUNT = 2;

    /** Positive (non-zero) time delay between the entity's animations. */
    private double animationPeriod;

    /** Positive (non-zero) time delay between the entity's behaviors. */
    private double behaviorPeriod;

    public Fairy(String id, Point position, List<PImage> images, double animationPeriod, double behaviorPeriod) {
        super(id, position, images);
        this.animationPeriod = animationPeriod;
        this.behaviorPeriod = behaviorPeriod;
    }

    @Override
    public void updateImage() {
        setImageIndex(getImageIndex() + 1);
    }

    /** Begins all animation updates for the entity. */
    @Override
    public void scheduleAnimation(EventScheduler scheduler, World world, ImageLibrary imageLibrary) {
        scheduler.scheduleEvent(this, new Animation(this, 0), animationPeriod);
    }

    @Override
    public void scheduleBehavior(EventScheduler scheduler, World world, ImageLibrary imageLibrary) {
        scheduler.scheduleEvent(this, new Behavior(this, world, imageLibrary), behaviorPeriod);
    }

    @Override
    public void scheduleActions(EventScheduler scheduler, World world, ImageLibrary imageLibrary) {
        // shares same functionality as Dude, Fairy, Sapling, Tree
        scheduleAnimation(scheduler, world, imageLibrary);
        scheduleBehavior(scheduler, world, imageLibrary);
    }
    /** Executes Fairy specific Logic. */
    @Override
    public void executeBehavior(World world, ImageLibrary imageLibrary, EventScheduler scheduler) {
        Optional<Entity> fairyTarget = world.findNearest(getPosition(), new ArrayList<>(List.of(Stump.class)));

        if (fairyTarget.isPresent()) {
            Point tgtPos = fairyTarget.get().getPosition();

            if (moveTo(world, fairyTarget.get(), scheduler)) {
                Entity sapling = new Sapling(Sapling.SAPLING_KEY + "_" + fairyTarget.get().getId(), tgtPos, imageLibrary.get(Sapling.SAPLING_KEY), Sapling.SAPLING_BEHAVIOR_PERIOD);

                world.addEntity(sapling);
                sapling.scheduleActions(scheduler, world, imageLibrary);
            }
        }

        scheduleBehavior(scheduler, world, imageLibrary);
    }

    /** Attempts to move the Fairy toward a target, returning True if already adjacent to it. */
    @Override
    public boolean moveTo(World world, Entity target, EventScheduler scheduler) {
        if (getPosition().adjacentTo(target.getPosition())) {
            world.removeEntity(scheduler, target);
            return true;
        } else {
            Point nextPos = nextPosition(world, target.getPosition());
            if (!getPosition().equals(nextPos)) {
                world.moveEntity(scheduler, this, nextPos);
            }
            return false;
        }
    }

    /** Determines a Fairy's next position when moving. */
    @Override
    public Point nextPosition(World world, Point destination) {
        Predicate<Point> canPassThrough = point -> world.inBounds(point) && !(world.isOccupied(point));
        BiPredicate<Point, Point> withinReach = (start, goal) -> start.adjacentTo(goal);

        // A pathing strategy instantiation
        PathingStrategy pathingStrategy = new AStarPathingStrategy();
        List<Point> path = pathingStrategy.computePath(getPosition(), destination, canPassThrough, withinReach, PathingStrategy.CARDINAL_NEIGHBORS);

        if (path.isEmpty()) {
            // Logic if there is no path or at the destination
            return getPosition();
        }
        // Logic if there is a path
        return path.get(0);

    }

    @Override
    public double getAnimationPeriod() {
        return animationPeriod;
    }

}
