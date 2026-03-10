package ca.jrvs.apps.grep;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class JavaGrepLambdaImp extends JavaGrepImp {

  private static final Logger logger = LoggerFactory.getLogger(JavaGrepLambdaImp.class);

  @Override
  public void process() throws IOException {
    logger.info("Starting JavaGrepLambdaImp: regex={}, rootPath={}, outFile={}",
        getRegex(), getRootPath(), getOutFile());

    List<String> matchedLines = listFiles(getRootPath()).stream()
        .flatMap(file -> {
          try {
            return readLines(file).stream();
          } catch (IOException e) {
            throw new RuntimeException("Failed to read file: " + file, e);
          }
        })
        .filter(this::containsPattern)
        .collect(Collectors.toList());

    writeToFile(matchedLines);
    logger.info("Finished JavaGrepLambdaImp. Matched lines={}", matchedLines.size());
  }

  @Override
  public void writeToFile(List<String> lines) throws IOException {
    Path outPath = Paths.get(getOutFile());
    Path parent = outPath.getParent();

    if (parent != null && !Files.exists(parent)) {
      Files.createDirectories(parent);
    }

    try (BufferedWriter writer = Files.newBufferedWriter(outPath)) {
      for (String line : lines) {
        writer.write(line);
        writer.newLine();
      }
    }
  }
}
