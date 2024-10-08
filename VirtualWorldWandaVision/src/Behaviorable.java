public interface Behaviorable {
    /** Schedules a single behavior update for the entity. */
    void scheduleBehavior(EventScheduler scheduler, World world, ImageLibrary imageLibrary);

    /** Performs the entity's behavior logic. */
    void executeBehavior(World world, ImageLibrary imageLibrary, EventScheduler scheduler);


}