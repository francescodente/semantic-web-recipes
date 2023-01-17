import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.ModelFactory;
import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.Resource;

import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class RdfGenerator {
    private List<Recipe> recipes;
    public RdfGenerator(List<Recipe> recipes) {
        this.recipes = recipes;
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

    private Stream<String> measurementUnitsDefinition(){
        return recipes.stream()
                .flatMap(r-> r.getIngredients().stream())
                .map(i-> i.getMeasurementUnit())
                .distinct()
                .map(u-> mesUnitRDF(u));
                //.collect(Collectors.joining("\n"));
    }

    private Stream<String> dishesDefinition(){
        return recipes.stream().map(r-> r.getDish()).distinct().map(d-> dishUnitRDF(d));
    }


    public void generate(){
        System.out.println(measurementUnitsDefinition());
    }
}
