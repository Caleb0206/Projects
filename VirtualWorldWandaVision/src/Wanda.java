import processing.core.PImage;

import java.util.List;
import java.util.Optional;
import java.util.function.BiPredicate;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Stream;

public class Wanda extends Entity implements Transformable, Moveable, Behaviorable, Animatable{

    public static final String WANDA_KEY = "wanda";

    public static final double DEFAULT_BEHAVIOR_PERIOD = 1.0;
    public static final double DEFAULT_ANIMATION_PERIOD = 0.5;

    public static final int DEFAULT_RECOURSE_LIMIT = 1;



    /** Positive (non-zero) time delay between the entity's animations. */
    private double animationPeriod;

    /** Positive (non-zero) time delay between the entity's behaviors. */
    private double behaviorPeriod;

    /** Number of resources collected by the entity. */
    private int resourceCount;

    /** Total number of resources the entity may hold. */
    private int resourceLimit;

    public Wanda(String id, Point position, List<PImage> images, double animationPeriod, double behaviorPeriod, int resourceCount, int resourceLimit) {
        super(id, position, images);
        this.animationPeriod = animationPeriod;
        this.behaviorPeriod = behaviorPeriod;
        this.resourceCount = resourceCount;
        this.resourceLimit = resourceLimit;
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
        // shares same functionality as Dude, Fairy, Sapling, Tree
        scheduleAnimation(scheduler, world, imageLibrary);
        scheduleBehavior(scheduler, world, imageLibrary);
    }

    @Override
    public void executeBehavior(World world, ImageLibrary imageLibrary, EventScheduler scheduler) {
        Optional<Entity> wandaTarget = findWandaTarget(world);
        if (wandaTarget.isEmpty())
            return;
        Point tgtPos = wandaTarget.get().getPosition();
        Background hex = new Background("hex_bg", imageLibrary.get("hex_bg"), 0);
        boolean fairyOrMushroom = moveTo(world, wandaTarget.get(), scheduler);


        if (wandaTarget.isEmpty() || !fairyOrMushroom || !transform(world, scheduler, imageLibrary))
        {
            if(world.inBounds(getPosition()) && ! world.getBackgroundCell(getPosition()).getId().equals("ruins_bg"))
                world.setBackgroundCell(getPosition(), hex);
            scheduleBehavior(scheduler, world, imageLibrary);
        }
        else if(fairyOrMushroom)
        {
            if (wandaTarget.isPresent() && wandaTarget.get() instanceof Mushroom)
            {
                if (world.inBounds(tgtPos)) {
                    Entity wandaVisionHouse = new WandaVisionHouse(WandaVisionHouse.WANDA_VISION_HOUSE_KEY,
                            tgtPos, imageLibrary.get(WandaVisionHouse.WANDA_VISION_HOUSE_KEY));
                    world.removeEntityAt(tgtPos);
                    world.addEntity(wandaVisionHouse);
                    wandaVisionHouse.scheduleActions(scheduler, world, imageLibrary);
                }
            }
        }
    }
    /** Returns the (optional) entity a Wanda will path toward. */
    public Optional<Entity> findWandaTarget(World world) {
        List<Class<?>> potentialTargets;

        if (resourceCount == resourceLimit) {
            // when Wanda has eaten enough fairies, will go to a Mushroom and transform the mushroom to a Vision
            potentialTargets = List.of(Mushroom.class);
        } else {
            // will target Fairies
            potentialTargets = List.of(Fairy.class);
        }

        return world.findNearest(getPosition(), potentialTargets);
    }


    @Override
    public boolean moveTo(World world, Entity target, EventScheduler scheduler) {
        Function<Point, Stream<Point>> potentialNeighbors = PathingStrategy.CARDINAL_NEIGHBORS;
        List<Point> neighbors = potentialNeighbors.apply(getPosition())
                .filter(world::inBounds)
                .filter(world::isOccupied)
                .filter(p -> world.getOccupant(p).get() instanceof House)
                .toList();
        if (!neighbors.isEmpty())
        {
            for(Point nPoint: neighbors) {
                if (world.getOccupant(nPoint).get() instanceof House) {
                    House tempHouse = (House) world.getOccupant(nPoint).get();
                    tempHouse.setHealth(0);
                }
            }
        }
        if (getPosition().adjacentTo(target.getPosition()) && world.inBounds(target.getPosition())) {
            world.removeEntityAt(target.getPosition());
            // Wanda removes either a Fairy or a Mushroom
            return true;
        }
        else {
            Point nextPos = nextPosition(world, target.getPosition());

            if (!getPosition().equals(nextPos)) {
                world.moveEntity(scheduler, this, nextPos);

            }

            return false;
        }
    }

    /** Determines Wanda's next position when moving. */
    @Override
    public Point nextPosition(World world, Point destination) {
        Predicate<Point> canPassThrough = point -> world.inBounds(point) && (!world.isOccupied(point)
                || (world.getOccupant(point).get() instanceof Stump)
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
    public boolean transform(World world, EventScheduler scheduler, ImageLibrary imageLibrary) {
        if (resourceCount < resourceLimit) {
            resourceCount = resourceCount + 1;

            if (resourceCount == resourceLimit) {
                Entity wanda = new Wanda(getId(), getPosition(), imageLibrary.get(WANDA_KEY + "_power"), animationPeriod, behaviorPeriod, resourceCount, resourceLimit);

                world.removeEntity(scheduler, this);

                world.addEntity(wanda);
                wanda.scheduleActions(scheduler, world, imageLibrary);

                return true;
            }
        } else {
            Entity wanda = new Wanda(getId(), getPosition(), imageLibrary.get(WANDA_KEY), animationPeriod, behaviorPeriod, 0, resourceLimit);

            world.removeEntity(scheduler, this);

            world.addEntity(wanda);
            wanda.scheduleActions(scheduler, world, imageLibrary);

            return true;
        }

        return false;


    }

    @Override
    public double getAnimationPeriod() {
        return animationPeriod;
    }
}
