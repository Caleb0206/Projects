public class Animation extends Action{

    public Animation(Entity entity, int repeatCount) {
        super(entity, null, null, repeatCount);
        // animation only needs entity and repeatCount
    }


    /** Performs 'Animation' specific logic. */
    @Override
    public void execute(EventScheduler scheduler) {
        ((Animatable)getEntity()).updateImage();

        if (getRepeatCount() != 1) {
            scheduler.scheduleEvent(getEntity(), new Animation(getEntity(), Math.max(getRepeatCount() - 1, 0)), ((Animatable)getEntity()).getAnimationPeriod());
        }
    }


}
