import processing.core.PImage;

import java.util.List;

public abstract class HealthEntity extends Entity{
    /** Entity that has Health: Tree and Sapling */
    private int health; // Entity's current health level

    public HealthEntity(String id, Point position, List<PImage> images, int health) {
        super(id, position, images);
        this.health = health;
    }
    public int getHealth() {
        return health;
    }

    public void setHealth(int health) {
        this.health = health;
    }
}
