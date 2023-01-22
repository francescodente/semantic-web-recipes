import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.ModelFactory;
import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.Resource;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
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
                "        <rdfs:label>"+unit+"</rdfs:label>\n" +
                "    </owl:NamedIndividual>";
    }
    private String dishUnitRDF(Dish dish){
        return "    <!-- http://www.semanticweb.org/it/unibo/semantic-web/recipes#"+nameToID(dish.getName())+" -->\n" +
                "\n" +
                "    <owl:NamedIndividual rdf:about=\"http://www.semanticweb.org/it/unibo/semantic-web/recipes#"+nameToID(dish.getName())+"\">\n" +
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
                "        <rdfs:label>" + ingName + "</rdfs:label>\n" +
                "    </owl:NamedIndividual>";
    }

    private String recipeIngredientRDF(Ingredient ingredient) {
        return "        <recipes:hasIngredientWithQuantity>\n" +
                "            <rdf:Description>\n" +
                "                <recipes:hasIngredient rdf:resource=\"http://www.semanticweb.org/it/unibo/semantic-web/recipes#"+nameToID(ingredient.getName())+"\"/>\n" +
                "                <recipes:hasMeasurementUnit rdf:resource=\"http://www.semanticweb.org/it/unibo/semantic-web/recipes#" + ingredient.getMeasurementUnit() + "\"/>\n" +
                "                <recipes:hasQuantity>" + ingredient.getQuantity() + "</recipes:hasQuantity>\n" +
                "            </rdf:Description>\n" +
                "        </recipes:hasIngredientWithQuantity>\n";
    }

    private String recipeUnitRDF(Recipe recipe){
        String ingredientsRDF = recipe.getIngredients().stream()
                .map(this::recipeIngredientRDF)
                .collect(Collectors.joining("\n"));
        return "    <!-- http://www.semanticweb.org/it/unibo/semantic-web/recipes#"+nameToID(recipe.getTitle())+" -->\n" +
                "\n" +
                "    <owl:NamedIndividual rdf:about=\"http://www.semanticweb.org/it/unibo/semantic-web/recipes#"+nameToID(recipe.getTitle())+"\">\n" +
                "        <recipes:isRecipeFor rdf:resource=\"http://www.semanticweb.org/it/unibo/semantic-web/recipes#"+ nameToID(recipe.getDish().getName()) +"\"/>\n" +
                "        <rdf:type rdf:resource=\"http://www.semanticweb.org/it/unibo/semantic-web/recipes#Recipe\"/>\n" +
                "        <recipes:hasInitialStep>\n"+
                         stepsUnitRDF(recipe.getSteps(), 0)+
                "        </recipes:hasInitialStep>\n"+
                "        <recipes:hasDifficulty>"+recipe.getDifficulty()+"</recipes:hasDifficulty>\n" +
                "        <recipes:hasPreparationTimeInMinutes rdf:datatype=\"http://www.w3.org/2001/XMLSchema#int\">"+recipe.getCookingTime()+"</recipes:hasPreparationTimeInMinutes>\n" +
                "        <recipes:hasTitle>"+recipe.getTitle()+"</recipes:hasTitle>\n" +
                "        " + ingredientsRDF +
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

    private String genHeader(){
        String h = "<?xml version=\"1\" encoding=\"UTF-8\"?>\n" +
                "<rdf:RDF\n" +
                "\txmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n" +
                "\txmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\"\n" +
                "\txmlns:sesame=\"http://www.openrdf.org/schema/sesame#\"\n" +
                "\txmlns:owl=\"http://www.w3.org/2002/07/owl#\"\n" +
                "\txmlns:xsd=\"http://www.w3.org/2001/XMLSchema#\"\n" +
                "\txmlns:fn=\"http://www.w3.org/2005/xpath-functions#\"\n" +
                "\txmlns:foaf=\"http://xmlns.com/foaf/0.1/\"\n" +
                "\txmlns:dc=\"http://purl.org/dc/elements/1.1/\"\n" +
                "\txmlns:hint=\"http://www.bigdata.com/queryHints#\"\n" +
                "\txmlns:bd=\"http://www.bigdata.com/rdf#\"\n" +
                "\txmlns:bds=\"http://www.bigdata.com/rdf/search#\"\n" +
                "\txmlns:psn=\"http://www.wikidata.org/prop/statement/value-normalized/\"\n" +
                "\txmlns:pqn=\"http://www.wikidata.org/prop/qualifier/value-normalized/\"\n" +
                "\txmlns:prn=\"http://www.wikidata.org/prop/reference/value-normalized/\"\n" +
                "\txmlns:mwapi=\"https://www.mediawiki.org/ontology#API/\"\n" +
                "\txmlns:gas=\"http://www.bigdata.com/rdf/gas#\"\n" +
                "\txmlns:wdt=\"http://www.wikidata.org/prop/direct/\"\n" +
                "\txmlns:wdtn=\"http://www.wikidata.org/prop/direct-normalized/\"\n" +
                "\txmlns:psv=\"http://www.wikidata.org/prop/statement/value/\"\n" +
                "\txmlns:ps=\"http://www.wikidata.org/prop/statement/\"\n" +
                "\txmlns:pqv=\"http://www.wikidata.org/prop/qualifier/value/\"\n" +
                "\txmlns:pq=\"http://www.wikidata.org/prop/qualifier/\"\n" +
                "\txmlns:prv=\"http://www.wikidata.org/prop/reference/value/\"\n" +
                "\txmlns:pr=\"http://www.wikidata.org/prop/reference/\"\n" +
                "\txmlns:wdno=\"http://www.wikidata.org/prop/novalue/\"\n" +
                "\txmlns:p=\"http://www.wikidata.org/prop/\"\n" +
                "\txmlns:wikibase=\"http://wikiba.se/ontology#\"\n" +
                "\txmlns:wd=\"http://www.wikidata.org/entity/\"\n" +
                "\txmlns:wdata=\"http://www.wikidata.org/wiki/Special:EntityData/\"\n" +
                "\txmlns:wds=\"http://www.wikidata.org/entity/statement/\"\n" +
                "\txmlns:wdv=\"http://www.wikidata.org/value/\"\n" +
                "\txmlns:wdref=\"http://www.wikidata.org/reference/\"\n" +
                "\txmlns:schema=\"http://schema.org/\"\n" +
                "\txmlns:prov=\"http://www.w3.org/ns/prov#\"\n" +
                "\txmlns:skos=\"http://www.w3.org/2004/02/skos/core#\"\n" +
                "\txmlns:geo=\"http://www.opengis.net/ont/geosparql#\"\n" +
                "\txmlns:geof=\"http://www.opengis.net/def/geosparql/function/\"\n" +
                "\txmlns:mediawiki=\"https://www.mediawiki.org/ontology#\"\n" +
                "\txmlns:ontolex=\"http://www.w3.org/ns/lemon/ontolex#\"\n" +
                "\txmlns:dct=\"http://purl.org/dc/terms/\"\n" +
                "    xmlns:recipes=\"http://www.semanticweb.org/it/unibo/semantic-web/recipes#\">";
        return h;
    }

    private String genFooter(){
        return "\n</rdf:RDF>";
    }

    private void write_to_file(String filepath, String content){
        try {
            FileWriter myWriter = new FileWriter(filepath);
            myWriter.write(content);
            myWriter.close();
            System.out.println("Successfully wrote to the file.");
        } catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
    }

    public void generate(String filepath){
        String res = genHeader() +
                Stream.of(measurementUnitsDefinition(), allDishesDefinition(), allRecipesDefinition(), allIngredientsDefinition())
                        .flatMap(s->s)
                        .collect(Collectors.toList())
                        .toString()
                + genFooter();
        write_to_file(filepath, res);

    }
}
