package ca.jrvs.apps.practice;

/**
 * Regex exercise interface.
 */
public interface RegexExc {

  /**
   * @return true if filename extension is jpg or jpeg (case insensitive)
   * @param filename input file name
   */
  boolean matchJpeg(String filename);

  /**
   * @return true if ip is valid
   * to simplify the problem, IP address range is from 0.0.0.0 to 999.999.999.999
   * @param ip input ip string
   */
  boolean matchIp(String ip);

  /**
   * @return true if line is empty (e.g. empty, white space, tabs, etc...)
   * @param line input line
   */
  boolean isEmptyLine(String line);
}
