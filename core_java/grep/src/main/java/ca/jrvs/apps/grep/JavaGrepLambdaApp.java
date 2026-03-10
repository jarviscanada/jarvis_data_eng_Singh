package ca.jrvs.apps.grep;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class JavaGrepLambdaApp {

  private static final Logger logger = LoggerFactory.getLogger(JavaGrepLambdaApp.class);

  public static void main(String[] args) {
    if (args.length != 3) {
      logger.error("USAGE: regex rootPath outFile");
      logger.error("Example: \".*Romeo.*Juliet.*\" ./data ./out/lambda_out.txt");
      System.exit(1);
    }

    JavaGrep grep = new JavaGrepLambdaImp();
    grep.setRegex(args[0]);
    grep.setRootPath(args[1]);
    grep.setOutFile(args[2]);

    try {
      grep.process();
    } catch (Exception e) {
      logger.error("Lambda grep failed", e);
      System.exit(2);
    }
  }
}
