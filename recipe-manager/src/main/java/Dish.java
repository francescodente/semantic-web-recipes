import java.util.Objects;

public class Dish {
    private String origin;
    private String name;

    public Dish(String name, String origin) {
        super();
        this.origin = origin;
        this.name = name;
    }

    public String getOrigin() {
        return origin;
    }

    public String getName() {
        return name;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Dish dish = (Dish) o;
        return Objects.equals(origin, dish.origin) &&
                Objects.equals(name, dish.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(origin, name);
    }

    @Override
    public String toString() {
        return "Dish{" +
                "origin='" + origin + '\'' +
                ", name='" + name + '\'' +
                '}';
    }
}


