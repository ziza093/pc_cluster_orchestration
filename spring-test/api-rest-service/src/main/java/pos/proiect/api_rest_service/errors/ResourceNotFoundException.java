package pos.proiect.api_rest_service.errors;

public class ResourceNotFoundException extends RuntimeException{
  public ResourceNotFoundException(String resource, String id){
    super(resource + " " + id + " not found");
  }
} 
