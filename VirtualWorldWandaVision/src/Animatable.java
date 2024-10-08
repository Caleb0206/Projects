public interface Animatable {
        /** Begins all animation updates for the entity. */
        void scheduleAnimation(EventScheduler scheduler, World world, ImageLibrary imageLibrary);

        void updateImage();
        double getAnimationPeriod();
}
