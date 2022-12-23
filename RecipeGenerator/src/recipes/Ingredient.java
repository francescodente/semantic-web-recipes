package recipes;

public class Ingredient {
	private double quantity;
	private String measurementUnit;
	private String name;
	
	public Ingredient(double quantity, String measurementUnit, String name) {
		super();
		this.quantity = quantity;
		this.measurementUnit = measurementUnit;
		this.name = name;
	}
	@Override
	public String toString() {
		return "Ingredient: \n[quantity=" + quantity + ",\n"+ " measurementUnit=" + measurementUnit+ ",\n" + " name=" + name + "]\n\n";
	}
	public double getQuantity() {
		return quantity;
	}
	public String getMeasurementUnit() {
		return measurementUnit;
	}
	public String getName() {
		return name;
	}


}
