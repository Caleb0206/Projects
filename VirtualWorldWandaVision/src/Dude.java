import processing.core.PImage;

import java.util.List;
import java.util.Optional;
import java.util.function.BiPredicate;
import java.util.function.Predicate;

public class Dude extends Entity implements Transformable, Moveable, Behaviorable, Animatable {
    public static final String DUDE_KEY = "dude";

    public static final int DUDE_PARSE_PROPERTY_BEHAVIOR_PERIOD_INDEX = 0;
    public static final int DUDE_PARSE_PROPERTY_ANIMATION_PERIOD_INDEX = 1;
    public static final int DUDE_PARSE_PROPERTY_RESOURCE_LIMIT_INDEX = 2;
    public static final int DUDE_PARSE_PROPERTY_COUNT = 3;

    /** Positive (non-zero) time delay between the entity's animations. */
    private double animationPeriod;

    /** Positive (non-zero) time delay between the entity's behaviors. */
    private double behaviorPeriod;

    /** Number of resources collected by the entity. */
    private int resourceCount;

    /** Total number of resources the entity may hold. */
    private int resourceLimit;


    public Dude(String id, Point position, List<PImage> images, double animationPeriod, double behaviorPeriod, int resourceCount, int resourceLimit) {
        super(id, position, images);
        // position, images, animationPeriod, behaviorPeriod, resourceCount, resourceLimit
        this.animationPeriod = animationPeriod;
        this.behaviorPeriod = behaviorPeriod;
        this.resourceCount = resourceCount;
        this.resourceLimit = resourceLimit;
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


    @Override
    public void executeBehavior(World world, ImageLibrary imageLibrary, EventScheduler scheduler) {
        Optional<Entity> dudeTarget = findDudeTarget(world);
        if (dudeTarget.isEmpty() || !moveTo(world, dudeTarget.get(), scheduler) || !transform(world, scheduler, imageLibrary)) {
            scheduleBehavior(scheduler, world, imageLibrary);
        }
    }


    /** Returns the (optional) entity a Dude will path toward. */
    public Optional<Entity> findDudeTarget(World world) {
        List<Class<?>> potentialTargets;

        if (resourceCount == resourceLimit) {
            potentialTargets = List.of(House.class, WandaVisionHouse.class);

        } else {
            potentialTargets = List.of(Tree.class, Sapling.class);
        }

        return world.findNearest(getPosition(), potentialTargets);
    }

    /** Attempts to move the Dude toward a target, returning True if already adjacent to it. */
    @Override
    public boolean moveTo(World world, Entity target, EventScheduler scheduler) {
        if (getPosition().adjacentTo(target.getPosition())) {
            if (target instanceof Tree tree) {
                tree.setHealth(tree.getHealth() - 1);
            } else if (target instanceof Sapling sapling) {
                sapling.setHealth(sapling.getHealth() - 1);
            }
            return true;
        } else {
            Point nextPos = nextPosition(world, target.getPosition());

            if (!getPosition().equals(nextPos)) {
                world.moveEntity(scheduler, this, nextPos);
            }

            return false;
        }
    }

    /** Determines a Dude's next position when moving. */
    @Override
    public Point nextPosition(World world, Point destination) {
        Predicate<Point> canPassThrough = point -> world.inBounds(point) && (!world.isOccupied(point) || (world.getOccupant(point).get() instanceof Stump));
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
    public boolean transform(World world, EventScheduler scheduler, ImageLibrary imageLibrary) {
        String imageStr = DUDE_KEY;
        if(getId().contains("_bw"))
            imageStr += "_bw";

        if (resourceCount < resourceLimit) {
            resourceCount = resourceCount + 1;

            if (resourceCount == resourceLimit) {

                Entity dude = new Dude(getId(), getPosition(), imageLibrary.get(imageStr + "_carry"), animationPeriod, behaviorPeriod, resourceCount, resourceLimit);

                world.removeEntity(scheduler, this);

                world.addEntity(dude);
                dude.scheduleActions(scheduler, world, imageLibrary);

                return true;
            }
        } else {
            Entity dude = new Dude(getId(), getPosition(), imageLibrary.get(imageStr), animationPeriod, behaviorPeriod, 0, resourceLimit);

            world.removeEntity(scheduler, this);

            world.addEntity(dude);
            dude.scheduleActions(scheduler, world, imageLibrary);

            return true;
        }

        return false;
    }
    @Override
    public double getAnimationPeriod() {
        return animationPeriod;
    }
    public int getResourceCount()
    {
        return resourceCount;
    }
    public int getResourceLimit()
    {
        return resourceLimit;
    }
    public double getBehaviorPeriod() {
        return behaviorPeriod;
    }
}
