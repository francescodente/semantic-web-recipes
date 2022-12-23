package recipes;

public class MainClass {

	public static void main(String[] args) {
		RecipeReader reader = new RecipeReader();
		reader.setFile("recipe1.txt");	
		System.out.println("Origin:" + reader.getOrigin());
		System.out.println("Time:" + reader.getTime());
		System.out.println("Ingredients");
		reader.getIngredients().forEach(line-> System.out.println(line));
		System.out.println("Directions");
		reader.getDirections().forEach(line-> System.out.println(line));
	}
}
