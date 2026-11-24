package pos.proiect.api_rest_service.computer;

import org.springframework.hateoas.EntityModel;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import jakarta.validation.Valid;

import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RequestMapping;

import pos.proiect.api_rest_service.errors.ResourceNotFoundException;
import pos.proiect.api_rest_service.computer.dto.ComputerResponse;
import pos.proiect.api_rest_service.computer.dto.ComputerRequest;



@RestController
@RequestMapping("/api/manager/computers")
class ComputerController {
    private final ComputerModelAssembler assembler;
    private final ComputerService service;

    ComputerController(ComputerService service, ComputerModelAssembler assembler){
        this.service = service;
        this.assembler = assembler;
    }   

    //maintainer
    // @GetMapping
    // List<Computer> all(){
    //     return assembler.toModel(service.findAll());
    // }

    @GetMapping("/{id}")
    public EntityModel<ComputerResponse> getComputerById(@RequestParam String id) {
        return assembler.toModel(service.get(id));
    }
    

    //only admin users
    @PostMapping
    public EntityModel<ComputerResponse> newComputer(@Valid @RequestBody ComputerRequest newComputer){
        return assembler.toModel(service.create(newComputer));
    }

    //only admin users can edit computers
    // @PutMapping("/api/manager/computers/{id}")
    // Computer replaceComputer(@RequestBody Computer newComputer, String id){
    //     return repository.findById(id).map(computer -> {
    //         computer.setIp(newComputer.getIp());
    //         computer.setHostname(newComputer.getHostname());
    //         return repository.save(computer);
    //     }).orElseGet( () -> {
    //         return repository.save(newComputer);
    //     });//idk
    // }

}
