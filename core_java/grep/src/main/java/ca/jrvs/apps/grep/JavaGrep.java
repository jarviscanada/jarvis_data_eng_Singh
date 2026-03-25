package ca.jrvs.apps.grep;

import java.io.IOException;
import java.util.stream.Stream;

public interface JavaGrep {

  void setRegex(String regex);
  void setRootPath(String rootPath);
  void setOutFile(String outFile);

  String getRegex();
  String getRootPath();
  String getOutFile();

  void process() throws IOException;

  Stream<String> readLines(String inputFile) throws IOException;

  Stream<String> listFiles(String rootDir) throws IOException;

  boolean containsPattern(String line);

  void writeToFile(Stream<String> lines) throws IOException;
}
