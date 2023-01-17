import java.util.List;
import java.util.Objects;

import static java.lang.String.valueOf;

public class Recipe {
    private Dish dish;
    private String title;
    private Integer cookingTime;
    private String difficulty;
    private List<Ingredient> ingredients;
    private List<String> steps;

    public Recipe(Dish dish, String title, Integer cookingTime, String difficulty, List<Ingredient> ingredients, List<String> steps) {
        super();
        this.cookingTime = cookingTime;
        this.ingredients = ingredients;
        this.steps = steps;
        this.dish = dish;
        this.title = title;
        this.difficulty = difficulty;
    }

    public String getDifficulty() {
        return difficulty;
    }
    public Dish getDish() {
        return dish;
    }
    public String getIDName() {
        return this.getTitle()
                .replaceAll(" ", "")
                .replaceAll("\\(", "")
                .replaceAll("\\)", "");
    }
    public String getTitle() {
        return title;
    }

    public Integer getCookingTime() {
        return cookingTime;
    }
    public List<Ingredient> getIngredients() {
        return ingredients;
    }
    public List<String> getSteps() {
        return steps;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Recipe recipe = (Recipe) o;
        return  Objects.equals(dish, recipe.dish) &&
                Objects.equals(title, recipe.title) &&
                Objects.equals(cookingTime, recipe.cookingTime) &&
                Objects.equals(difficulty, recipe.difficulty) &&
                Objects.equals(ingredients, recipe.ingredients) &&
                Objects.equals(steps, recipe.steps);
    }

    @Override
    public int hashCode() {
        return Objects.hash(dish, title, cookingTime, difficulty, ingredients, steps);
    }

}
