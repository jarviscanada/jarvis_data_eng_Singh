package ca.jrvs.apps.grep;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Collectors;
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

    List<String> matchedLines;
    try {
      matchedLines = listFiles(getRootPath()).stream()
          .flatMap(file -> {
            try {
              return readLines(file).stream();
            } catch (IOException e) {
              throw new UncheckedIOException("Failed to read file: " + file, e);
            }
          })
          .filter(this::containsPattern)
          .collect(Collectors.toList());
    } catch (UncheckedIOException e) {
      throw e.getCause();
    }

    writeToFile(matchedLines);
    logger.info("Finished JavaGrepLambdaImp. Matched lines={}", matchedLines.size());
  }

  @Override
  public List<String> readLines(String inputFile) throws IOException {
    try (Stream<String> lines = Files.lines(Paths.get(inputFile))) {
      return lines.collect(Collectors.toList());
    }
  }

  @Override
  public List<String> listFiles(String rootDir) throws IOException {
    Path root = Paths.get(rootDir);

    if (!Files.exists(root)) {
      throw new IllegalArgumentException("rootPath does not exist: " + rootDir);
    }

    try (Stream<Path> paths = Files.walk(root)) {
      return paths
          .filter(Files::isRegularFile)
          .map(Path::toString)
          .collect(Collectors.toList());
    }
  }
}
