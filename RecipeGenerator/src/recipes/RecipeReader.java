package recipes;
import java.io.File;  // Import the File class
import java.io.FileNotFoundException;  // Import this class to handle errors
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner; // Import the Scanner class to read text files

public class RecipeReader {
private File myFile;
private Scanner myScanner;
private String filename;


public RecipeReader() {
	super();
}

public void setFile(String filename) {
	this.filename = filename;
	this.myFile = new File(filename);
	
}

private List<String> readfield(String fieldTitle) {
	this.myScanner = new Scanner(ClassLoader.getSystemResourceAsStream(filename));
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

public List<String>getIngredients() {
	return readfield("Ingredients");
}

public List<String>getDirections(){
	return readfield("Directions");
}

public String getOrigin(){
	return readfield("Origin").get(0);
}

public int getTime(){
	return Integer.parseInt(readfield("Time").get(0));
}




	
	
	
}
