package pos.proiect.api_rest_service.computer;

import org.springframework.data.mongodb.repository.MongoRepository;;

interface ComputerRepository extends MongoRepository<Computer, Long>{

}