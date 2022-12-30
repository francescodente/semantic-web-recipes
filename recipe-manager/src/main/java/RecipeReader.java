import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Collectors;

public class RecipeReader {
    private Scanner myScanner;

    public Recipe read(String filepath) {
        File myFile = new File(filepath);
        String dish = this.readfield(myFile, "Dish").get(0);
        String title = this.readfield(myFile, "Title").get(0);
        String origin = this.readfield(myFile, "Origin").get(0);
        int time = Integer.parseInt(readfield(myFile, "Time").get(0));
        readfield(myFile,"Ingredients").stream().forEach(ingLine-> this.parseIngredient(ingLine));

        List<Ingredient> ingredients = this.readfield(myFile, "Ingredients").stream()
                .map(ingLine -> this.parseIngredient(ingLine))
                .collect(Collectors.toList());
        List<String> steps = readfield(myFile,"Directions");
        return new Recipe(dish, title, origin, time, ingredients, steps);
    }


    private List<String> readfield(File file, String fieldTitle) {
        try {
            this.myScanner = new Scanner(file);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        List<String> fieldData = new ArrayList<>();
        String line;
        Boolean readingRightLines = false;
        while(myScanner.hasNextLine()) {
            line = myScanner.nextLine();
            if(line.equals(fieldTitle)) {
                readingRightLines = true;
            }else if(readingRightLines && !line.isEmpty()){
                if(line.contains("<<<<")) {
                    return fieldData;
                }else {
                    fieldData.add(line);
                }
            }

        }
        return fieldData;
    }

    private Ingredient parseIngredient(String ingLine) {
        String[] line = ingLine.split(" ");

        double quantity = Double.parseDouble(line[0]);
        String measurmentUnit = line[1];
        String ingName = ingLine.substring(line[0].length()+line[1].length()+1);

        return new Ingredient(quantity, measurmentUnit , ingName);
    }



}
