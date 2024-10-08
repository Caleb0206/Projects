import processing.core.PImage;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.function.BiPredicate;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Stream;

public class Vision extends Entity implements Moveable, Behaviorable, Animatable{

    public static final String VISION_KEY = "vision";

    public static final double DEFAULT_BEHAVIOR_PERIOD = 1.0;
    public static final double DEFAULT_ANIMATION_PERIOD = 0.5;

    public static final int DEFAULT_RECOURSE_LIMIT = 1;



    /** Positive (non-zero) time delay between the entity's animations. */
    private double animationPeriod;

    /** Positive (non-zero) time delay between the entity's behaviors. */
    private double behaviorPeriod;


    public Vision(String id, Point position, List<PImage> images, double animationPeriod, double behaviorPeriod) {
        super(id, position, images);
        this.animationPeriod = animationPeriod;
        this.behaviorPeriod = behaviorPeriod;

    }

    @Override
    public void updateImage() {
        setImageIndex(getImageIndex() + 1);
    }

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
        scheduleAnimation(scheduler, world, imageLibrary);
        scheduleBehavior(scheduler, world, imageLibrary);
    }

    @Override
    public void executeBehavior(World world, ImageLibrary imageLibrary, EventScheduler scheduler) {
        Optional<Entity> visionTarget = findVisionTarget(world);

        if (visionTarget.isPresent()) {
            Point tgtPos = visionTarget.get().getPosition();

            if (moveTo(world, visionTarget.get(), scheduler)) {
                Entity visionFairy = new Fairy(Fairy.FAIRY_KEY + "_" + visionTarget.get().getId(), tgtPos, imageLibrary.get(Fairy.FAIRY_KEY), 1.0, 2.5);

                world.removeEntityAt(tgtPos);
                world.addEntity(visionFairy);
                visionFairy.scheduleActions(scheduler, world, imageLibrary);
            }
        }

        scheduleBehavior(scheduler, world, imageLibrary);

    }
    /** Returns the (optional) entity Vision will path toward. */
    public Optional<Entity> findVisionTarget(World world) {
        List<Class<?>> potentialTargets;

        // will target Stumps
        potentialTargets = List.of(Stump.class);

        return world.findNearest(getPosition(), potentialTargets);
    }


    @Override
    public boolean moveTo(World world, Entity target, EventScheduler scheduler) {

        if (getPosition().adjacentTo(target.getPosition())) {
            return true;
        } else {
            Point nextPos = nextPosition(world, target.getPosition());

            if (!getPosition().equals(nextPos)) {
                world.moveEntity(scheduler, this, nextPos);

            }

            return false;
        }
    }

    /** Determines Vision's next position when moving. */
    @Override
    public Point nextPosition(World world, Point destination) {
        Predicate<Point> canPassThrough = point -> world.inBounds(point) && (!world.isOccupied(point)
                || (world.getOccupant(point).get() instanceof Tree)
                || (world.getOccupant(point).get() instanceof Sapling));

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
