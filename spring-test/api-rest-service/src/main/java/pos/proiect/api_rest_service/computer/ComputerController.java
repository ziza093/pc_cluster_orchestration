package pos.proiect.api_rest_service.computer;

import org.springframework.hateoas.EntityModel;
import org.springframework.hateoas.CollectionModel;
import org.springframework.hateoas.IanaLinkRelations;


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

import org.springframework.http.ResponseEntity;

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
    @GetMapping
    public CollectionModel<EntityModel<ComputerResponse>> getComputers() {
        return assembler.toCollectionModel(service.findAll());
    }

    //maintainer
    @GetMapping("/{id}")
    public EntityModel<ComputerResponse> getComputerById(@PathVariable String id){
        return assembler.toModel(service.get(id));
    }
    

    //only admin users
    @PostMapping
    public ResponseEntity<EntityModel<ComputerResponse>> newComputer(@Valid @RequestBody ComputerRequest request){
        EntityModel<ComputerResponse> model = assembler.toModel(service.create(request));
        return ResponseEntity
                .created(model.getRequiredLink(IanaLinkRelations.SELF).toUri())
                .body(model);
    }

    //only admin users can edit computers
    @PutMapping("/{id}")
    public ResponseEntity<EntityModel<ComputerResponse>> replaceComputer(@PathVariable String id, @Valid @RequestBody ComputerRequest request){
        service.update(id, request);
        return ResponseEntity.noContent().build();
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<EntityModel<ComputerResponse>> deleteComputer(@PathVariable String id){
        service.delete(id);
        return ResponseEntity.ok().build();
    }
}
