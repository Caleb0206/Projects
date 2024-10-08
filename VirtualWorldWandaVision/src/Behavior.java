public class Behavior extends Action{

    public Behavior(Entity entity, World world, ImageLibrary imageLibrary) {
        super(entity, world, imageLibrary, 0);
        // Behavior only needs entity, world, imageLibrary
    }

    /** Performs 'Behavior' specific logic. */
    public void execute(EventScheduler scheduler) {
        ((Behaviorable)getEntity()).executeBehavior(getWorld(), getImageLibrary(), scheduler);

    }

//    /**
//     * Returns a new 'Behavior' type action.
//     * Constructor arguments provide hints to data necessary for a subclass.
//     *
//     * @param entity The entity enacting the behavior.
//     * @param world The world in which the behavior occurs.
//     * @param imageLibrary The image data that may be used by the behavior.
//     *
//     * @return A new Action object configured as a(n) 'Behavior'.
//     */
//    public static Action createBehavior(Entity entity, World world, ImageLibrary imageLibrary) {
//        return new Action(ActionKind.BEHAVIOR, entity, world, imageLibrary, 0);
//    }
}
