package pos.proiect.api_rest_service.computer;

import pos.proiect.api_rest_service.computer.dto.ComputerResponse;

import org.springframework.hateoas.server.RepresentationModelAssembler;
import org.springframework.stereotype.Component;
import static org.springframework.hateoas.server.mvc.WebMvcLinkBuilder.linkTo;
import static org.springframework.hateoas.server.mvc.WebMvcLinkBuilder.methodOn;

import org.bson.types.ObjectId;
import org.springframework.hateoas.EntityModel;


@Component 
public class ComputerModelAssembler implements RepresentationModelAssembler<Computer, EntityModel<ComputerResponse>>{
    
    @Override
    public EntityModel<ComputerResponse> toModel(Computer computer){
        ComputerResponse response = new ComputerResponse(
            computer.getId(),
            computer.getIp(),
            computer.getHostname(),
            computer.getIdScripts().stream().map(ObjectId::toHexString).toList(),
            computer.getIdUsers().stream().map(ObjectId::toHexString).toList()
        );
        return EntityModel.of(response,
            linkTo(methodOn(ComputerController.class).getComputerById(computer.getId())).withSelfRel(),
            linkTo(ComputerController.class).withRel("parent"));
            
    }
}
