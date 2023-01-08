import java.util.List;

import static java.lang.String.valueOf;

public class Recipe {
    private String origin;
    private String dish;
    private String title;
    private Integer cookingTime;
    private String difficulty;
    private List<Ingredient> ingredients;
    private List<String> steps;

    public Recipe(String dish, String title, String origin, Integer cookingTime, String difficulty, List<Ingredient> ingredients, List<String> steps) {
        super();
        this.origin = origin;
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
    public String getOrigin() {
        return origin;
    }
    public String getDish() {
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

}
