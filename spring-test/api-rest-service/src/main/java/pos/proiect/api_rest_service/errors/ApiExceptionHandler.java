package pos.proiect.api_rest_service.errors;

import java.time.Instant;
import java.util.LinkedHashMap;
import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import jakarta.servlet.http.HttpServletRequest;


@RestControllerAdvice
public class ApiExceptionHandler{

  @ExceptionHandler(ResourceNotFoundException.class)
  public ResponseEntity<ErrorResponse> notFound(ResourceNotFoundException ex, HttpServletRequest req){
    return build(HttpStatus.NOT_FOUND, ex.getMessage(), null, req);
  }

  @ExceptionHandler(MethodArgumentNotValidException.class)
  public ResponseEntity<ErrorResponse> invalid(MethodArgumentNotValidException ex, HttpServletRequest req) {
    Map<String, String> details = new LinkedHashMap<>();
    ex.getBindingResult().getFieldErrors()
      .forEach(e -> details.putIfAbsent(e.getField(), e.getDefaultMessage()));
    return build(HttpStatus.UNPROCESSABLE_CONTENT, "Validation failed", details, req);
  }

  @ExceptionHandler(DuplicateKeyException.class)
  public ResponseEntity<ErrorResponse> duplicate(DuplicateKeyException ex, HttpServletRequest req) {
    return build(HttpStatus.CONFLICT, "ip or hostname already exists", null, req);
  }

  private ResponseEntity<ErrorResponse> build(HttpStatus status, String message, Map<String, String> details, HttpServletRequest req) {
    ErrorResponse body = new ErrorResponse(Instant.now(), status.value(), status.getReasonPhrase(), message, req.getRequestURI(), details);
    return ResponseEntity.status(status).body(body);
  }
}