package pos.proiect.api_rest_service.computer;

import java.util.List;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;


@RestController
class ComputerController {
    private final ComputerRepository repository;
    
    ComputerController(ComputerRepository repository){
        this.repository = repository;
    }

    //Agregate root
    //tag::get-aggregate-root[]
    @GetMapping("/computers")
    List<Computer> all(){
        return repository.findAll();
    }
    //end::get-aggregate-root[]

    @PostMapping("/computers")
    Computer newComputer(@RequestBody Computer newComputer){
        return repository.save(newComputer);
    }

    //Single item

    @GetMapping("/computers/{id}")
    Computer one(@PathVariable Long id){
        return repository.findById(id).orElseThrow(() -> new ComputerNotFoundException(id));
    }

    @PutMapping("/computers/{id}")
    Computer replaceComputer(@RequestBody Computer newComputer, @PathVariable Long id){
        return repository.findById(id).map(computer -> {
            computer.setIp(newComputer.getIp());
            computer.setHostname(newComputer.getHostname());
            return repository.save(computer);
        })
        .orElseGet(() -> {
            return repository.save(newComputer);
        });
    }

    @DeleteMapping("/computers/{id}")
    void deleteComputer(@PathVariable Long id){
        repository.deleteById(id);
    }

}
