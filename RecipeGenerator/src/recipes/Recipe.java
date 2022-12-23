package recipes;
import java.util.List;
public class Recipe {
	private String origin;
	private String dish;
	private String title;
	private Integer cookingTime;
	private List<Ingredient> ingredients;
	private List<String> steps;

	public Recipe(String dish, String title,String origin, Integer cookingTime, List<Ingredient> ingredients, List<String> steps) {
		super();
		this.origin = origin;
		this.cookingTime = cookingTime;
		this.ingredients = ingredients;
		this.steps = steps;
		this.dish = dish;
		this.title = title;
	}
	
	public String getOrigin() {
		return origin;
	}
	public String getDish() {
		return dish;
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
