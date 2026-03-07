package ca.jrvs.apps.grep;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class JavaGrepImp implements JavaGrep {

  private static final Logger logger = LoggerFactory.getLogger(JavaGrepImp.class);

  private String regex;
  private String rootPath;
  private String outFile;

  private Pattern pattern;

  @Override
  public void setRegex(String regex) {
    this.regex = regex;
    this.pattern = Pattern.compile(regex);
  }

  @Override
  public void setRootPath(String rootPath) {
    this.rootPath = rootPath;
  }

  @Override
  public void setOutFile(String outFile) {
    this.outFile = outFile;
  }

  @Override
  public String getRegex() {
    return regex;
  }

  @Override
  public String getRootPath() {
    return rootPath;
  }

  @Override
  public String getOutFile() {
    return outFile;
  }

  @Override
  public void process() throws IOException {
    if (regex == null || rootPath == null || outFile == null) {
      throw new IllegalArgumentException("regex, rootPath, and outFile must be set before process()");
    }
    if (pattern == null) {
      pattern = Pattern.compile(regex);
    }

    logger.info("Starting JavaGrep: regex={}, rootPath={}, outFile={}", regex, rootPath, outFile);

    List<String> matchedLines = new ArrayList<>();

    for (String file : listFiles(rootPath)) {
      for (String line : readLines(file)) {
        if (containsPattern(line)) {
          matchedLines.add(line);
        }
      }
    }

    writeToFile(matchedLines);
    logger.info("JavaGrep finished. Matched lines={}", matchedLines.size());
  }

  @Override
  public List<String> readLines(String inputFile) throws IOException {
    return Files.readAllLines(Paths.get(inputFile));
  }

  @Override
  public List<String> listFiles(String rootDir) throws IOException {
    Path root = Paths.get(rootDir);

    if (!Files.exists(root)) {
      throw new IllegalArgumentException("rootPath does not exist: " + rootDir);
    }

    List<String> files = new ArrayList<>();
    Files.walk(root)
        .filter(Files::isRegularFile)
        .forEach(p -> files.add(p.toString()));

    return files;
  }

  @Override
  public boolean containsPattern(String line) {
    if (line == null) return false;
    return pattern.matcher(line).find();
  }

  @Override
  public void writeToFile(List<String> lines) throws IOException {
    Path outPath = Paths.get(outFile);

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
