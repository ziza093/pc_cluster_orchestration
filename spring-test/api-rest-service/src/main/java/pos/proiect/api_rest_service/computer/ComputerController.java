package pos.proiect.api_rest_service.computer;

import java.util.List;

// import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
// import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
// import org.springframework.web.bind.annotation.PutMapping;
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
    @GetMapping("/api/manager/computers")
    List<Computer> all(){
        return repository.findAll();
    }
    //end::get-aggregate-root[]he name RFC 9110 uses and your lab text matches. Use whichever your version offers, and if neither compiles, HttpStatus.valueOf(422) works.

    @PostMapping("/computers")
    Computer newComputer(@RequestBody Computer newComputer){
        return repository.save(newComputer);
    }


    //TODO: pt model assembler
    @PostMapping("/{id")
    public String getComputerById(@RequestBody String entity) {
        //TODO: process POST request
        
        return entity;
    }
    

    //Single item

    // @GetMapping("/computers/{id}")
    // Computer one(@PathVariable Long id){
    //     return repository.findById(id).orElseThrow(() -> new ApiExceptionHandler(id));
    // }

    // @PutMapping("/computers/{id}")
    // Computer replaceComputer(@RequestBody Computer newComputer, @PathVariable Long id){
    //     return repository.findById(id).map(computer -> {
    //         computer.setIp(newComputer.getIp());
    //         computer.setHostname(newComputer.getHostname());
    //         return repository.save(computer);
    //     })
    //     .orElseGet(() -> {
    //         return repository.save(newComputer);
    //     });
    // }

    // @DeleteMapping("/computers/{id}")
    // void deleteComputer(@PathVariable Long id){
    //     repository.deleteById(id);
    // }

}
