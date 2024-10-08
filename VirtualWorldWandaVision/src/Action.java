/** A scheduled action to be carried out by a specific entity. */
public abstract class Action {
    /**
     * Enumerated type defining different kinds of actions that entities take in the world.
     * Specific values are assigned to the action's 'kind' instance variable at initialization.
     * There are two types of actions: animations (image updates) and behaviors (logic updates).
     */


    /** Entity enacting the action. */
    private final Entity entity;
    /** World in which the action occurs. */
    private final World world;
    /** Image data that may be used by the action. */
    private final ImageLibrary imageLibrary;
    /** Number of animation repeats. A zero indicates indefinite repeats. */
    private int repeatCount;

    /**
     * Constructs an Action object with specified characteristics.
     * In the base program, this is not called directly.
     * Instead, the encapsulated 'create' method are used to create specific kinds.
     *
     * @param entity The entity enacting the action.
     * @param world The world in which the action occurs.
     * @param imageLibrary The image data that may be used by the action.
     * @param repeatCount The number of animation repeats. A zero indicates indefinite repeats.
     */
    public Action(Entity entity, World world, ImageLibrary imageLibrary, int repeatCount) {
        this.entity = entity;
        this.world = world;
        this.imageLibrary = imageLibrary;
        this.repeatCount = repeatCount;
    }


    /** Called when the action's scheduled time occurs. */
    public abstract void execute(EventScheduler scheduler);

    public Entity getEntity() {
        return entity;
    }
    public World getWorld() {
        return world;
    }
    public ImageLibrary getImageLibrary() {
        return imageLibrary;
    }
    public int getRepeatCount() {
        return repeatCount;
    }



}
