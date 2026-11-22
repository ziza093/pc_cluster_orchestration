package pos.proiect.api_rest_service.computer;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
class LoadDatabase {

  private static final Logger log = LoggerFactory.getLogger(LoadDatabase.class);

  @Bean
  CommandLineRunner initDatabase(ComputerRepository repository) {

    return args -> {
      log.info("Preloading " + repository.save(new Computer("10.11.12.13", "home")));
      log.info("Preloading " + repository.save(new Computer("14.15.16.17", "school")));
    };
  }
}