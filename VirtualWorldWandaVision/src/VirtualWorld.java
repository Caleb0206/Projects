import java.util.*;
import java.util.function.Function;
import java.util.stream.Stream;

import processing.core.*;

public final class VirtualWorld extends PApplet {
    public static final int TILE_WIDTH = 32;
    public static final int TILE_HEIGHT = 32;
    public static final int VIEW_WIDTH = 512;
    public static final int VIEW_HEIGHT = 288;
    public static final int VIEW_SCALE = 2;
    public static final int VIEW_COLS = VIEW_WIDTH / TILE_WIDTH;
    public static final int VIEW_ROWS = VIEW_HEIGHT / TILE_HEIGHT;
    public static final String IMAGE_LIST_FILE_NAME = "imagelist";
    public static final int DEFAULT_IMAGE_COLOR = 0x808080;
    public static final String FAST_FLAG = "-fast";
    public static final String FASTER_FLAG = "-faster";
    public static final String FASTEST_FLAG = "-fastest";
    public static final String WORLD_STRING_FLAG = "-string";
    public static final double FAST_SCALE = 0.5;
    public static final double FASTER_SCALE = 0.25;
    public static final double FASTEST_SCALE = 0.0625;
    private static String[] ARGS;
    public String worldString = "world";
    public boolean worldStringIsFilePath = true;
    public long startTimeMillis = 0;
    public double timeScale = 1.0;

    public ImageLibrary imageLibrary;
    public World world;
    public WorldView view;
    public EventScheduler scheduler;

    /** Entrypoint that runs the Processing applet. */
    public static void main(String[] args) {
        VirtualWorld.ARGS = args;
        PApplet.main(VirtualWorld.class);
    }

    /** Performs an entire VirtualWorld simulation for testing. */
    public static List<String> headlessMain(String[] args, double lifetime){
        VirtualWorld.ARGS = args;

        VirtualWorld virtualWorld = new VirtualWorld();
        virtualWorld.setup();
        virtualWorld.update(lifetime);

        return virtualWorld.world.log();
    }

    /** Settings for pixelated graphics */
    public void settings() {
        noSmooth();
        size(VIEW_WIDTH * VIEW_SCALE, VIEW_HEIGHT * VIEW_SCALE);
    }

    /** Processing entry point for "sketch" setup. */
    public void setup() {
        parseCommandLine(ARGS);

        loadImageLibrary(IMAGE_LIST_FILE_NAME);
        loadWorld(worldString, imageLibrary);

        view = new WorldView(VIEW_ROWS, VIEW_COLS, this, VIEW_SCALE, world, TILE_WIDTH, TILE_HEIGHT);
        scheduler = new EventScheduler();
        startTimeMillis = System.currentTimeMillis();

        scheduleActions(world, scheduler, imageLibrary);
    }

    /** Handles command line arguments. */
    public void parseCommandLine(String[] args) {
        for (String arg : args) {
            switch (arg) {
                case FAST_FLAG -> timeScale = Math.min(FAST_SCALE, timeScale);
                case FASTER_FLAG -> timeScale = Math.min(FASTER_SCALE, timeScale);
                case FASTEST_FLAG -> timeScale = Math.min(FASTEST_SCALE, timeScale);
                case WORLD_STRING_FLAG -> worldStringIsFilePath = false;
                default -> worldString = arg;
            }
        }
    }

    /** Loads the image library. */
    public void loadImageLibrary(String filename) {
        imageLibrary = new ImageLibrary(ImageLibrary.createImageColored(TILE_WIDTH, TILE_HEIGHT, DEFAULT_IMAGE_COLOR));
        imageLibrary.loadFromFile(filename, this);
    }

    /** Loads the world. */
    public void loadWorld(String loadString, ImageLibrary imageLibrary) {
        if (worldStringIsFilePath) {
            world = WorldParser.createFromFile(loadString, imageLibrary);
        } else {
            world = WorldParser.createFromString(loadString, imageLibrary);
        }
    }

    /** Called to start all entity's actions and behaviors when the program starts. */
    public void scheduleActions(World world, EventScheduler scheduler, ImageLibrary imageLibrary) {
        for (Entity entity : world.getEntities()) {
            entity.scheduleActions(scheduler, world, imageLibrary);
        }
    }

    /** Called multiple times automatically per second. */
    public void draw() {
        double appTime = (System.currentTimeMillis() - startTimeMillis) * 0.001;
        double frameTime = appTime / timeScale - scheduler.getCurrentTime();
        update(frameTime);
        view.drawViewport();
    }

    /** Performs update logic. */
    public void update(double frameTime){
        scheduler.updateOnTime(frameTime);
    }

    /** Mouse press input handling. */
    public void mousePressed() {
        Point pressed = mouseToPoint();
         System.out.println("Click Location (" + pressed.x + ", " + pressed.y + ")");

        Entity wanda = new Wanda(
                Wanda.WANDA_KEY,
                pressed,
                imageLibrary.get(Wanda.WANDA_KEY),
                Wanda.DEFAULT_ANIMATION_PERIOD,
                Wanda.DEFAULT_BEHAVIOR_PERIOD,
                0,
                Wanda.DEFAULT_RECOURSE_LIMIT
        );
        Function<Point, Stream<Point>> potentialNeighbors = PathingStrategy.CARDINAL_NEIGHBORS;
        Background ruins = new Background("ruins_bg", imageLibrary.get("ruins_bg"), 0);
        if (world.isOccupied( pressed )) {
            world.removeEntityAt(pressed);
        }

        world.addEntity(wanda);
        wanda.scheduleActions(scheduler, world, imageLibrary);

        world.setBackgroundCell(pressed, ruins);

        List<Point> neighbors = potentialNeighbors.apply(pressed)
                .filter(world::inBounds)
                .toList();
        for (Point nPoint : neighbors) {
            if(world.isOccupied(nPoint))
            {
                // if water surrounds Wanda, remove it
                if ( world.getOccupant(nPoint).get() instanceof Water)
                    world.removeEntityAt(nPoint);
                else if (world.getOccupant(nPoint).get() instanceof Dude)
                {

                    // if Dude is around Wanda, change to b&w Dude
                    Dude d = (Dude) world.getOccupant(nPoint).get();
                    Entity bw_dude = new Dude(d.getId() + "_bw", d.getPosition(), imageLibrary.get(Dude.DUDE_KEY + "_bw"),
                            d.getAnimationPeriod(), d.getBehaviorPeriod(), d.getResourceCount(), d.getResourceLimit());

                    world.removeEntity(scheduler, d); // Remove the original Dude entity
                    world.addEntity(bw_dude); // Add the new black-and-white Dude entity
                    bw_dude.scheduleActions(scheduler, world, imageLibrary);


                }
            }

            world.setBackgroundCell(nPoint, ruins);
        }

    }

    /** Converts mouse position to world position. */
    private Point mouseToPoint() {
        return view.getViewport().viewportToWorld(mouseX / TILE_WIDTH / VIEW_SCALE, mouseY / TILE_HEIGHT / VIEW_SCALE);
    }

    /** Keyboard input handling. */
    public void keyPressed() {
        if (key == CODED) {
            int dx = 0;
            int dy = 0;

            switch (keyCode) {
                case UP -> dy -= 1;
                case DOWN -> dy += 1;
                case LEFT -> dx -= 1;
                case RIGHT -> dx += 1;
            }

            view.shiftView(dx, dy);
        }
    }

}
