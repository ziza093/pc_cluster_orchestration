package pos.proiect.api_rest_service.computer;


class ComputerNotFoundException extends RuntimeException {

  ComputerNotFoundException(Long id) {
    super("Could not find employee " + id);
  }
}