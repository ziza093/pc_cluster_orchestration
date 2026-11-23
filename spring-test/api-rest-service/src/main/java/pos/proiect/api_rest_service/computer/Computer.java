package pos.proiect.api_rest_service.computer;

import java.util.List;
import java.util.ArrayList;

import org.bson.types.ObjectId;
// import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;
import org.springframework.data.mongodb.core.mapping.FieldType;
import org.springframework.data.mongodb.core.mapping.MongoId;

@Document(collection = "computers")
public class Computer{

    @MongoId(FieldType.OBJECT_ID)
    private String id;
    
    @Indexed(unique = true)
    @Field("IP")
    private String ip;

    @Indexed(unique = true, sparse = true)
    @Field("hostname")
    private String hostname;

    @Field("id_scripts")
    private List<ObjectId> idScripts = new ArrayList<>();
    
    @Field("id_users")
    private List<ObjectId> idUsers = new ArrayList<>();

    Computer() {}

    Computer(String ip, String hostname){
        this.ip = ip;
        this.hostname = hostname;
        this.idScripts = new ArrayList<>();
        this.idUsers = new ArrayList<>();
    }

    public String getId(){ return this.id; }
    public void setId(String id){ this.id = id; }

    public String getIp(){ return this.ip; }
    public void setIp(String ip){ this.ip = ip; }

    public String getHostname(){ return this.hostname; }
    public void setHostname(String hostname){ this.hostname = hostname; }
    
    public List<ObjectId> getIdScripts(){ return this.idScripts; }
    public void setIdScripts(List<ObjectId> idScripts){ this.idScripts = idScripts; }

    public List<ObjectId> getIdUsers(){ return this.idUsers; }
    public void setIdUsers(List<ObjectId> idUsers){ this.idUsers = idUsers; }

    public void addScript(ObjectId scriptId) { this.idScripts.add(scriptId); }
    public void removeScript(ObjectId scriptId) { this.idScripts.remove(scriptId); }

    public void addUser(ObjectId userId) { this.idUsers.add(userId); }
    public void removeUser(ObjectId userId) { this.idUsers.remove(userId); }


    
    @Override
    public String toString(){
        return "Computer [id=" + id + ", ip=" + ip + ", hostname=" + hostname + ", scripts=" + idScripts + ", users=" + idUsers + "]";
    }
}
