package pos.proiect.api_rest_service.computer;

import java.util.List;

import org.springframework.stereotype.Service;

import org.bson.types.ObjectId;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import pos.proiect.api_rest_service.computer.dto.ComputerRequest;
import pos.proiect.api_rest_service.errors.ResourceNotFoundException;

@Service 
public class ComputerService {
    
    private final ComputerRepository repository;

    public ComputerService(ComputerRepository repository){
        this.repository = repository;   
    }
    

    public Computer get(String id){
        if(!ObjectId.isValid(id)){
            throw new ResourceNotFoundException("Computer", id);
        }
        return repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Computer", id));
    }

    public List<Computer> findAll(){
        return repository.findAll();
    }

    public Page<Computer> findAll(Pageable pageable){
        return repository.findAll(pageable);
    }

    public Computer create(ComputerRequest req){
        Computer computer = new Computer();
        computer.setIp(req.ip());
        computer.setHostname(req.hostname());
        return repository.save(computer);
    }

    public Computer update(String id, ComputerRequest req){
        Computer computer = get(id);
        computer.setIp(req.ip());
        computer.setHostname(req.hostname());
        return repository.save(computer);    
    }

    public void delete(String id){
        repository.delete(get(id));
    }

}
