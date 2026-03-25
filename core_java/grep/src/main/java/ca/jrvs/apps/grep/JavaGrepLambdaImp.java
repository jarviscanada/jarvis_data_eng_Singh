package ca.jrvs.apps.grep;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.util.concurrent.atomic.AtomicLong;
import java.util.stream.Stream;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class JavaGrepLambdaImp extends JavaGrepImp {

  private static final Logger logger = LoggerFactory.getLogger(JavaGrepLambdaImp.class);

  @Override
  public void process() throws IOException {
    if (getRegex() == null || getRootPath() == null || getOutFile() == null) {
      throw new IllegalArgumentException("regex, rootPath, and outFile must be set before process()");
    }

    logger.info("Starting JavaGrepLambdaImp: regex={}, rootPath={}, outFile={}",
        getRegex(), getRootPath(), getOutFile());

    AtomicLong matchCount = new AtomicLong(0);

    try (Stream<String> matchedLines = listFiles(getRootPath())
        .flatMap(file -> {
          try {
            return readLines(file);
          } catch (IOException e) {
            throw new UncheckedIOException("Failed to read file: " + file, e);
          }
        })
        .filter(this::containsPattern)
        .peek(line -> matchCount.incrementAndGet())) {
      writeToFile(matchedLines);
    } catch (UncheckedIOException e) {
      throw e.getCause();
    }

    logger.info("Finished JavaGrepLambdaImp. Matched lines={}", matchCount.get());
  }
}
