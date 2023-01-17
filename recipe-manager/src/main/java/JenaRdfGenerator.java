
import com.hp.hpl.jena.datatypes.xsd.XSDDatatype;
import com.hp.hpl.jena.ontology.*;
import com.hp.hpl.jena.rdf.model.*;
import com.hp.hpl.jena.vocabulary.XSD;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


public class JenaRdfGenerator {
    OntModel model;
    String namespace;

    public JenaRdfGenerator() {
        model = ModelFactory.createOntologyModel(OntModelSpec.OWL_MEM_TRANS_INF);
        namespace = "http://www.semanticweb.org/dente/ontologies/2022/10/recipe-mgmt#";
    }

    public void newRecipe(){}
    public void newIngredient(){}
    public void newMeasurementUnit(){}
    public void newDish(){}

    private String capitalize(String word){
       return word.substring(0,1).toUpperCase() + word.substring(1);
    }

    private String genUriFromName(String className){
        return namespace + this.capitalize(className);
    }
    private OntClass getOntClassByName(String className){
        return model.getOntClass(genUriFromName(className));
    }

    private  DatatypeProperty getDtPropertyByName(String propertyName){
        return model.getDatatypeProperty(genUriFromName(propertyName));
    }

    private void createClasses(List<String> classes){
        classes.forEach(className ->model.createClass(genUriFromName(className)));
    }
    private void createDataProperties(String className, Map<String, Resource> dataPropNamesRanges){
        DatatypeProperty property;
        for(Map.Entry<String, Resource> propData : dataPropNamesRanges.entrySet()){
            property = model.createDatatypeProperty(genUriFromName(propData.getKey()));
            property.setDomain(getOntClassByName(className));
            property.setRange(propData.getValue());
        }
    }

    private void createObjectProperties(String className, Map<String, Resource> objPropNamesRanges) {
        ObjectProperty property;
        for(Map.Entry<String, Resource> propData : objPropNamesRanges.entrySet()){
            property = model.createObjectProperty(genUriFromName(propData.getKey()));
            property.setDomain(getOntClassByName(className));
            property.setRange(propData.getValue());
        }
    }
    public void ontologySetup(Recipe r){
        /*Create classes*/
        this.createClasses(Arrays.asList("recipe", "dish", "ingredient", "ingredientWithQuantity",
                                        "measurementUnit", "quantity", "step"));

        /*Create data properties*/

        //Recipe
        this.createDataProperties("recipe", new HashMap<String, Resource>(){{
                    put("hasPreparationTimeInMinutes", XSD.integer);
                    put("hasTitle", XSD.xstring);
                    put("hasDifficulty", XSD.xstring);
                }}
        );

        //Quantity
        this.createDataProperties("quantity", new HashMap<String, Resource>(){{
                    put("hasValue", XSD.xdouble);
                }}
        );

        //Step
        this.createDataProperties("step", new HashMap<String, Resource>(){{
                    put("hasDescription", XSD.xdouble);
                }}
        );

        /*Create object properties*/

        //Recipe
        this.createObjectProperties("recipe", new HashMap<String, Resource>(){{
                    put("containsIngredient", getOntClassByName("ingredient"));
                    put("hasIngredientWithQuantity", getOntClassByName("ingredientWithQuantity"));
                    put("isRecipeFor", getOntClassByName("dish"));
                    //TODO manca has step con sottoprop hasInitialStep
                }}
        );

        //Dish
        this.createObjectProperties("dish", new HashMap<String, Resource>(){{
                    put("hasRecipe", getOntClassByName("recipe"));
                }}
        );

        //Step
        this.createObjectProperties("step", new HashMap<String, Resource>(){{
                    put("happensAfter", getOntClassByName("step"));
                }}
        );

        /*Create individuals*/
            //TODO astrarre con un metodo
        Individual recipeIndividual = model.createIndividual(namespace + r.getIDName(), getOntClassByName("recipe"));
        Literal recTitleLit = model.createTypedLiteral(r.getIDName(), XSDDatatype.XSDstring);
        Statement recTitleSt = model.createStatement(recipeIndividual, getDtPropertyByName("hasTitle"), recTitleLit);
        model.add(recTitleSt);
        Literal recTimeLit = model.createTypedLiteral(r.getCookingTime(), XSDDatatype.XSDinteger);
        Statement recTimeSt = model.createStatement(recipeIndividual, getDtPropertyByName("hasPreparationTimeInMinutes"), recTimeLit);
        model.add(recTimeSt);



        try {
            model.write(new FileOutputStream(new File( System.getProperty("user.dir")+ "\\" +"src\\main\\resources\\recipesTest.owl")));
        } catch (FileNotFoundException e) {
            model.write(System.out);
        }
    }


    public void generate(Recipe recipe){
        String rootUri = "http://www.semanticweb.org/dente/ontologies/2022/10/recipe-mgmt#";
        String fullName = "BasicPancakes";

// create an empty Model
        Model model = ModelFactory.createDefaultModel();

// create the resource
        Resource recipeRes = model.createResource(rootUri + recipe.getIDName());
// add the property

        Property hasTitle = model.createProperty("http://www.semanticweb.org/dente/ontologies/2022/10/recipe-mgmt#", "hasTitle");
        Property hasDifficulty =  model.createProperty("http://www.semanticweb.org/dente/ontologies/2022/10/recipe-mgmt#", "hasDifficulty");
        recipeRes.addProperty(hasTitle, recipe.getTitle());
        recipeRes.addProperty(hasDifficulty, recipe.getDifficulty());
        model.write(System.out);
    }


}
