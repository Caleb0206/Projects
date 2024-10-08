import processing.core.PImage;

import java.util.List;
import java.util.function.Function;
import java.util.stream.Stream;

public class WandaVisionHouse extends Entity implements Behaviorable, Animatable, Transformable {
    public static final int WANDA_VISION_HOUSE_PARSE_PROPERTY_COUNT = 0;

    public static final String WANDA_VISION_HOUSE_KEY = "wanda_vision_house";
    private double behaviorPeriod;
    private double animationPeriod;

    private boolean spawnedVision;
    public WandaVisionHouse(String id, Point position, List<PImage> images) {
        super(id, position, images);
        behaviorPeriod = 0.6;
        animationPeriod = 3;
        spawnedVision = false;
    }
    @Override
    public void scheduleActions(EventScheduler scheduler, World world, ImageLibrary imageLibrary) {
        scheduleBehavior(scheduler, world, imageLibrary);
        scheduleAnimation(scheduler, world, imageLibrary);
    }

    @Override
    public void scheduleBehavior(EventScheduler scheduler, World world, ImageLibrary imageLibrary) {
        scheduler.scheduleEvent(this, new Behavior(this, world, imageLibrary), behaviorPeriod);
    }

    @Override
    public void executeBehavior(World world, ImageLibrary imageLibrary, EventScheduler scheduler) {
        Background bg = new Background("hex_bg", imageLibrary.get("hex_bg"), 0);
        if(world.inBounds(getPosition())) {
            world.setBackgroundCell(getPosition(), bg);

            if(!transform(world, scheduler, imageLibrary) && !spawnedVision)
            {
                // transform is false means Wandavision House is complete
                // spawn Vision
                Function<Point, Stream<Point>> potentialNeighbors = PathingStrategy.CARDINAL_NEIGHBORS;
                List<Point> neighbors = potentialNeighbors.apply(getPosition())
                        .filter(world::inBounds)
                        .filter(p -> !world.isOccupied(p))
                        .toList();

                // neighbors that are not occupied
                if (!neighbors.isEmpty()) {
                    // just get the first neighbor position
                    Point spawnVisionPoint = neighbors.get(0);
                    Vision vision = new Vision(Vision.VISION_KEY, spawnVisionPoint, imageLibrary.get(Vision.VISION_KEY),
                            Vision.DEFAULT_ANIMATION_PERIOD, Vision.DEFAULT_BEHAVIOR_PERIOD );

                    world.addEntity(vision);
                    scheduleActions(scheduler, world, imageLibrary);
                    vision.scheduleActions(scheduler, world, imageLibrary);
                    spawnedVision = true;
                }
            }
        }

//        }
        scheduleBehavior(scheduler, world, imageLibrary);
    }


    @Override
    public boolean transform(World world, EventScheduler scheduler, ImageLibrary imageLibrary) {
        if(getId().equals(WANDA_VISION_HOUSE_KEY)) {
            if (getImageIndex() + 1 < 5) {
                return true;
            } else {
                Entity buildWVHouse = new WandaVisionHouse(getId() + "_finished", getPosition(), imageLibrary.get(WANDA_VISION_HOUSE_KEY + "_finished"));
                world.removeEntity(scheduler, this);

                world.addEntity(buildWVHouse);
                buildWVHouse.scheduleActions(scheduler, world, imageLibrary);
            }
        }
        return false;
    }

    @Override
    public void scheduleAnimation(EventScheduler scheduler, World world, ImageLibrary imageLibrary) {
        if (getId().equals(WANDA_VISION_HOUSE_KEY))
            scheduler.scheduleEvent(this, new Animation(this, 0), animationPeriod);
    }

    @Override
    public void updateImage() {
        if (getId().equals(WANDA_VISION_HOUSE_KEY))
            setImageIndex(getImageIndex() + 1);
    }

    @Override
    public double getAnimationPeriod() {
        return animationPeriod;
    }
}
