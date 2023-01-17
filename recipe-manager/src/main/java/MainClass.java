import java.io.File;
import java.util.*;
import java.util.stream.Collectors;

import static java.lang.String.valueOf;

public class MainClass {

    public static void main(String[] args) {
        String folderPath = System.getProperty("user.dir")+ "\\" +"src\\main\\resources\\recipes";
        RecipeReader reader = new RecipeReader();
        List<Recipe> recipes = new ArrayList<>();
        File folder = new File(folderPath);

        Arrays.stream(Objects.requireNonNull(folder.listFiles()))
                .filter(file -> file.getName().endsWith(".txt"))
                .forEach(file -> recipes.add(reader.read(file.getPath())));


        //recipes.forEach(recipe-> System.out.println(recipe.getIDName()));

        RdfGenerator rdgen = new RdfGenerator(recipes);
        rdgen.generate();

    }
}
