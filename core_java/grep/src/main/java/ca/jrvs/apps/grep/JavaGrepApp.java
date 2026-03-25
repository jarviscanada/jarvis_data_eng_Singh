package ca.jrvs.apps.grep;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class JavaGrepApp {

  private static final Logger logger = LoggerFactory.getLogger(JavaGrepApp.class);

  public static void main(String[] args) {
    if (args.length != 3) {
      logger.error("USAGE: regex rootPath outFile");
      logger.error("Example: \".*Romeo.*Juliet.*\" ./data ./out/out.txt");
      System.exit(1);
    }

    String regex = args[0];
    String rootPath = args[1];
    String outFile = args[2];

    JavaGrep grep = new JavaGrepImp();
    grep.setRegex(regex);
    grep.setRootPath(rootPath);
    grep.setOutFile(outFile);

    try {
      grep.process();
    } catch (Exception e) {
      logger.error("Grep failed", e);
      System.exit(2);
    }
  }
}
