package ca.jrvs.apps.grep;

import java.io.IOException;
import java.util.List;

public interface JavaGrep {

  void setRegex(String regex);
  void setRootPath(String rootPath);
  void setOutFile(String outFile);

  String getRegex();
  String getRootPath();
  String getOutFile();

  void process() throws IOException;

  List<String> readLines(String inputFile) throws IOException;

  List<String> listFiles(String rootDir) throws IOException;

  boolean containsPattern(String line);

  void writeToFile(List<String> lines) throws IOException;
}
