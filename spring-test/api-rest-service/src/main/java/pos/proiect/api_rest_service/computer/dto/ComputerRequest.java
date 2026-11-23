package pos.proiect.api_rest_service.computer.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

public record ComputerRequest(
    
    @NotBlank
    @Pattern(
        regexp = "^(?:(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)\\.){3}(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)$",
        message = "must be a valid IPv4 address"
    ) 
    String ip,


    @Size(max=253) 
    @Pattern(
        regexp = "^[A-Za-z]([A-Za-z0-9-]*[A-Za-z0-9])?$",
        message = "must start with a letter, contain only letters, digits and hyphens, and not end with a hyphen"
    )
    String hostname

) { }
