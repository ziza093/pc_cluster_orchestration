package pos.proiect.api_rest_service.computer.dto;

import java.util.List;


public record ComputerResponse(

    String id,
    String ip,
    String hostname,
    List<String> idScripts,
    List<String> idUsers

) { }
