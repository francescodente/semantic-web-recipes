package recipes;

public class MainClass {

	public static void main(String[] args) {
		String path = System.getProperty("user.dir")+ "\\" + "recipe1.txt";
		RecipeReader reader = new RecipeReader();
		Recipe recipe = reader.read(path);	
		System.out.println("Origin: " + recipe.getOrigin());
		System.out.println("Time: " + recipe.getCookingTime());
		//System.out.println("Ingredients:\n " + recipe.getIngredients());		
	
		//recipe.getSteps().forEach(step-> System.out.println("Step\n" + step + "\n"));
		
	}
}
