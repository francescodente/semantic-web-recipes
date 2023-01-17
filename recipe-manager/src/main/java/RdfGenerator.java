import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.ModelFactory;
import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.Resource;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class RdfGenerator {
    private List<Recipe> recipes;
    private Map<String,String> allIngredients;
    public RdfGenerator(List<Recipe> recipes) {
        this.recipes = recipes;
        this.allIngredients = new HashMap<>();
        this.setIngredients();
    }

    private void setIngredients(){
        String path = System.getProperty("user.dir")+ "\\" +"src\\main\\resources\\ingredientsList.txt";
        File file = new File(path);
        String categoryID;
        String ingName;
        String line = "";
        try {
            Scanner myScanner = new Scanner(file);
            while(myScanner.hasNextLine()){
                line = myScanner.nextLine();
                categoryID = line.split("#")[0];
                ingName = line.split("#")[1];
                allIngredients.put(ingName, categoryID);
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }


    }

    private String nameToID(String name) {
        return name.replaceAll(" ", "_")
                .replaceAll("\\(", "_")
                .replaceAll("\\)", "_");
    }
    private String mesUnitRDF(String unit){
        return "    <!-- http://www.semanticweb.org/it/unibo/semantic-web/recipes#"+unit+"-->\n" +
                "\n" +
                "    <owl:NamedIndividual rdf:about=\"http://www.semanticweb.org/it/unibo/semantic-web/recipes#"+unit+"\">\n" +
                "        <rdf:type rdf:resource=\"http://www.semanticweb.org/it/unibo/semantic-web/recipes#MeasurementUnit\"/>\n" +
                "    </owl:NamedIndividual>";
    }
    private String dishUnitRDF(Dish dish){
        return "    <!-- http://www.semanticweb.org/it/unibo/semantic-web/recipes#"+nameToID(dish.getName())+" -->\n" +
                "\n" +
                "    <owl:NamedIndividual rdf:about=\"http://www.semanticweb.org/it/unibo/semantic-web/recipes#"+nameToID(dish.getName())+">\n" +
                "        <rdf:type rdf:resource=\"http://www.semanticweb.org/it/unibo/semantic-web/recipes#Dish\"/>\n" +
                "        <recipes:hasOrigin rdf:resource=\"http://www.wikidata.org/entity/"+dish.getOrigin()+"\"/>\n" +
                "        <rdfs:label>"+dish.getName()+"</rdfs:label>\n" +
                "    </owl:NamedIndividual>";
    }
    private String ingUnitRDF(String ingName){
        String foodonURI;

        if(allIngredients.containsKey(ingName))
            foodonURI = "http://purl.obolibrary.org/obo/FOODON_"+allIngredients.get(ingName);
        else foodonURI = "http://purl.org/heals/food/Food";

        return "    <!-- http://www.semanticweb.org/it/unibo/semantic-web/recipes#"+nameToID(ingName)+" -->\n" +
                "\n" +
                "    <owl:NamedIndividual rdf:about=\"http://www.semanticweb.org/it/unibo/semantic-web/recipes#"+nameToID(ingName)+"\">\n" +
                "        <rdf:type rdf:resource=\""+foodonURI+"\"/>\n" +
                "    </owl:NamedIndividual>";
    }
    private String recipeUnitRDF(Recipe recipe){ //TODO sistema initial step
        return "    <!-- http://www.semanticweb.org/it/unibo/semantic-web/recipes#"+nameToID(recipe.getTitle())+" -->\n" +
                "\n" +
                "    <owl:NamedIndividual rdf:about=\"http://www.semanticweb.org/it/unibo/semantic-web/recipes#"+nameToID(recipe.getTitle())+"\">\n" +
                "        <rdf:type rdf:resource=\"http://www.semanticweb.org/it/unibo/semantic-web/recipes#Recipe\"/>\n" +
                "        <recipes:hasInitialStep>\n"+
                         stepsUnitRDF(recipe.getSteps(), 0)+
                "        </recipes:hasInitialStep>\n"+
                "        <recipes:hasDifficulty>"+recipe.getDifficulty()+"</recipes:hasDifficulty>\n" +
                "        <recipes:hasPreparationTimeInMinutes rdf:datatype=\"http://www.w3.org/2001/XMLSchema#int\">"+recipe.getCookingTime()+"</recipes:hasPreparationTimeInMinutes>\n" +
                "        <recipes:hasTitle>"+recipe.getTitle()+"</recipes:hasTitle>\n" +
                "    </owl:NamedIndividual>";
    }

    private String nextGenerator(List<String> steps, int index){
        if(index!=steps.size()-1)
            return "        <recipes:hasNext>\n" +
                                stepsUnitRDF(steps,index+1) +
                    "        </recipes:hasNext>\n";
        else return "";
    }

    private String stepsUnitRDF(List<String> steps, int index){

        return "    <rdf:Description>\n" +
                "        <rdf:type rdf:resource=\"http://www.semanticweb.org/it/unibo/semantic-web/recipes#Step\"/>\n" +
                "        <recipes:hasDescription>"+steps.get(index)+"</recipes:hasDescription>\n" +
                        nextGenerator(steps, index) +
                "    </rdf:Description>";
    }

    private Stream<String> measurementUnitsDefinition(){
        return recipes.stream()
                .flatMap(r-> r.getIngredients().stream())
                .map(i-> i.getMeasurementUnit())
                .distinct()
                .map(u-> mesUnitRDF(u));
                //.collect(Collectors.joining("\n"));
    }
    private Stream<String> allIngredientsDefinition(){
        return recipes.stream()
                .flatMap(r-> r.getIngredients().stream())
                .map(i-> i.getName())
                .distinct()
                .map(n->ingUnitRDF(n));
    }
    private Stream<String> allDishesDefinition(){
        return recipes.stream().map(r-> r.getDish()).distinct().map(d-> dishUnitRDF(d));
    }
    private Stream<String> allRecipesDefinition(){
        return recipes.stream().map(r-> recipeUnitRDF(r));
    }

    public void generate(){
        Arrays.asList(measurementUnitsDefinition(), allDishesDefinition(), allRecipesDefinition(), allIngredientsDefinition())
                .stream().flatMap(s->s)
                .forEach(x-> System.out.println(x));


    }
}
