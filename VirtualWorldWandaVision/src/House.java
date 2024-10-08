import processing.core.PImage;

import java.util.List;

public class House extends HealthEntity implements Transformable, Behaviorable{
    public static final int HOUSE_PARSE_PROPERTY_COUNT = 2;

    public static final int HOUSE_PARSE_BEHAVIOR_PERIOD_INDEX = 0;
    public static final int HOUSE_PARSE_PROPERTY_HEALTH_INDEX = 1;
    public static final String HOUSE_KEY = "house";
    private double behaviorPeriod;

    public House(String id, Point position, List<PImage> images, double behaviorPeriod, int health) {
        super(id, position, images, health);
        this.behaviorPeriod = behaviorPeriod;
    }

    @Override
    public void scheduleBehavior(EventScheduler scheduler, World world, ImageLibrary imageLibrary) {
        scheduler.scheduleEvent(this, new Behavior(this, world, imageLibrary), behaviorPeriod);
    }
    @Override
    public void scheduleActions(EventScheduler scheduler, World world, ImageLibrary imageLibrary) {
        scheduleBehavior(scheduler, world, imageLibrary);
    }
    @Override
    public void executeBehavior(World world, ImageLibrary imageLibrary, EventScheduler scheduler) {
        if (!transform(world, scheduler, imageLibrary)) {
            scheduleBehavior(scheduler, world, imageLibrary);
        }
    }
    @Override
    public boolean transform(World world, EventScheduler scheduler, ImageLibrary imageLibrary) {
        if (getHealth() <= 0) {
            Entity wVHouse = new WandaVisionHouse(WandaVisionHouse.WANDA_VISION_HOUSE_KEY,
                            getPosition(), imageLibrary.get(WandaVisionHouse.WANDA_VISION_HOUSE_KEY));

            world.removeEntity(scheduler, this);

            world.addEntity(wVHouse);
            wVHouse.scheduleActions(scheduler, world, imageLibrary);

            return true;
        }

        return false;
    }
}
