import processing.core.PImage;

import java.util.List;

public class Sapling extends HealthEntity implements Transformable, Behaviorable, Animatable {
    public static final String SAPLING_KEY = "sapling";
    public static final int SAPLING_PARSE_PROPERTY_COUNT = 0;

    public static final int SAPLING_HEALTH_LIMIT = 5;
    public static final double SAPLING_BEHAVIOR_PERIOD = 2.0;
    public static final double SAPLING_ANIMATION_PERIOD = 0.01; // Very small to react to health changes

    /** Positive (non-zero) time delay between the entity's animations. */
    private double animationPeriod;
    /** Positive (non-zero) time delay between the entity's behaviors. */
    private double behaviorPeriod;


    public Sapling(String id, Point position, List<PImage> images, double behaviorPeriod) {
        super(id, position, images, 0);
        animationPeriod = SAPLING_ANIMATION_PERIOD;
        this.behaviorPeriod = behaviorPeriod;
    }

    /** Called when an animation action occurs. */
    @Override
    public void updateImage() {
        if (getHealth() <= 0) {
            setImageIndex(0);
        } else if (getHealth() < SAPLING_HEALTH_LIMIT) {
            setImageIndex(getImages().size() * getHealth() / SAPLING_HEALTH_LIMIT);
        } else {
            setImageIndex(getImages().size() - 1);
        }
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

    /** Called to begin animation and/or behavior for an entity. */
    @Override
    public void scheduleActions(EventScheduler scheduler, World world, ImageLibrary imageLibrary) {
        scheduleAnimation(scheduler, world, imageLibrary);
        scheduleBehavior(scheduler, world, imageLibrary);
    }


    /** Performs the entity's behavior logic. */
    @Override
    public void executeBehavior(World world, ImageLibrary imageLibrary, EventScheduler scheduler) {
        setHealth(getHealth() + 1);
        if (!transform(world, scheduler, imageLibrary)) {
            scheduleBehavior(scheduler, world, imageLibrary);
        }
    }

    /** Checks the Sapling's health and transforms accordingly, returning true if successful. */
    @Override
    public boolean transform(World world, EventScheduler scheduler, ImageLibrary imageLibrary) {
        if (getHealth() <= 0) {
            Entity stump = new Stump(Stump.STUMP_KEY + "_" + getId(), getPosition(), imageLibrary.get(Stump.STUMP_KEY));

            world.removeEntity(scheduler, this);

            world.addEntity(stump);

            return true;
        } else if (getHealth() >= SAPLING_HEALTH_LIMIT) {
            Entity tree = new Tree(
                    Tree.TREE_KEY + "_" + getId(),
                    getPosition(),
                    imageLibrary.get(Tree.TREE_KEY),
                    NumberUtil.getRandomDouble(Tree.TREE_RANDOM_ANIMATION_PERIOD_MIN, Tree.TREE_RANDOM_ANIMATION_PERIOD_MAX), NumberUtil.getRandomDouble(Tree.TREE_RANDOM_BEHAVIOR_PERIOD_MIN, Tree.TREE_RANDOM_BEHAVIOR_PERIOD_MAX),
                    NumberUtil.getRandomInt(Tree.TREE_RANDOM_HEALTH_MIN, Tree.TREE_RANDOM_HEALTH_MAX)
            );

            world.removeEntity(scheduler, this);

            world.addEntity(tree);
            tree.scheduleActions(scheduler, world, imageLibrary);

            return true;
        }

        return false;
    }

    @Override
    public double getAnimationPeriod() {
        return animationPeriod;
    }
}
