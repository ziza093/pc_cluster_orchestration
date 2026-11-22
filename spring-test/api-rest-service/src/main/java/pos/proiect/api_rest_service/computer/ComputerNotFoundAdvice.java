package pos.proiect.api_rest_service.computer;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
class ComputerNotFoundAdvice {

  @ExceptionHandler(ComputerNotFoundException.class)
  @ResponseStatus(HttpStatus.NOT_FOUND)
  String employeeNotFoundHandler(ComputerNotFoundException ex) {
    return ex.getMessage();
  }
}
