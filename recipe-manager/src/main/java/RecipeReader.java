import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Collectors;

public class RecipeReader {
    private Scanner myScanner;

    public Recipe read(String filePath) {
        File myFile = new File(filePath);
        String dish = this.readField(myFile, "Dish").get(0);
        String title = this.readField(myFile, "Title").get(0);
        String origin = this.readField(myFile, "Origin").get(0);
        int time = Integer.parseInt(readField(myFile, "Time").get(0));
        String difficulty = this.readField(myFile, "Difficulty").get(0);
        readField(myFile,"Ingredients").forEach(this::parseIngredient);

        List<Ingredient> ingredients = this.readField(myFile, "Ingredients").stream()
                .map(this::parseIngredient)
                .collect(Collectors.toList());
        List<String> steps = readField(myFile,"Directions");
        return new Recipe(dish, title, origin, time, difficulty, ingredients, steps);
    }




    private List<String> readField(File file, String fieldTitle) {
        try {
            this.myScanner = new Scanner(file);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        List<String> fieldData = new ArrayList<>();
        String line;
        boolean readingRightLines = false;
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
        String measurementUnit = line[1];
        String ingName = ingLine.substring(line[0].length()+line[1].length()+1);

        return new Ingredient(quantity, measurementUnit , ingName);
    }



}
