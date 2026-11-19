package pos.proiect.api_rest_service;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/users")
public class UserController{
    private List<String> users = List.of("Alice", "BOB", "Char");

    @GetMapping
    public List<String> getUsers() {
        
        // Returns JSON response
        return users; 
    }
}
