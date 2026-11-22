package pos.proiect.api_rest_service.computer;

import java.util.List;

//all these comments are because my clumsy brain can't get over the fact i didnt know how to create a ObjectId type var...
//at first create a simple h2database, than move to mongodb

// import org.bson.types.ObjectId;
// import org.springframework.data.annotation.Id;
// import org.springframework.data.mongodb.core.mapping.Document;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;

// @Document(collection = "computers")
@Entity
class Computer{

    // @Id
    // private ObjectId id;
    private @Id
    @GeneratedValue Long id;
    private String ip;
    private String hostname;
    // private List<ObjectId> idScript;
    // private List<ObjectId> idUser;
    private List<String> idScript;
    private List<String> idUser;

    Computer() {}

    Computer(String ip, String hostname){
        this.ip = ip;
        this.hostname = hostname;
    }

    // public ObjectId getId(){
    //     return this.id;
    // }
    public Long getId(){
        return this.id;
    }

    public String getIp(){
        return this.ip;
    }

    public String getHostname(){
        return this.hostname;
    }

    // public List<ObjectId> getIdScript(){
    //     return this.idScript;
    // }

    // public List<ObjectId> getIdUser(){
    //     return this.idUser;
    // }
     
    public List<String> getIdScript(){
        return this.idScript;
    }

    public List<String> getIdUser(){
        return this.idUser;
    }

    // public void setId(ObjectId id){
    //     this.id = id;
    // }
    public void setId(Long id){
        this.id = id;
    }

    public void setIp(String ip){
        this.ip = ip;
    }

    public void setHostname(String hostname){
        this.hostname = hostname;
    }

    // public void setIdScript(ObjectId idScript){
    //     this.idScript.add(idScript);
    // }

    // public void setIdUser(ObjectId idUser){
    //     this.idUser.add(idUser);
    // }
    public void setIdScript(String idScript){
        this.idScript.add(idScript);
    }

    public void setIdUser(String idUser){
        this.idUser.add(idUser);
    }
    
    @Override
    public String toString(){
        return "Computer [id=" + id + ", ip=" + ip + ", hostname=" + hostname + ", scripts=" + idScript + ", users=" + idUser;
    }
}
