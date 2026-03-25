package ca.jrvs.apps.practice;

import java.util.regex.Pattern;

public class RegexExcImp implements RegexExc {

  // Case-insensitive: jpg or jpeg at end of string
  private static final Pattern JPEG_PATTERN =
      Pattern.compile("^.+\\.(jpe?g)$", Pattern.CASE_INSENSITIVE);

  // Simplified IP: 4 groups of 1-3 digits separated by dots (0-999 each)
  private static final Pattern IP_PATTERN =
      Pattern.compile("^(\\d{1,3}\\.){3}\\d{1,3}$");

  // Empty or whitespace-only line
  private static final Pattern EMPTY_LINE_PATTERN =
      Pattern.compile("^\\s*$");

  @Override
  public boolean matchJpeg(String filename) {
    if (filename == null) return false;
    return JPEG_PATTERN.matcher(filename).matches();
  }

  @Override
  public boolean matchIp(String ip) {
    if (ip == null) return false;
    return IP_PATTERN.matcher(ip).matches();
  }

  @Override
  public boolean isEmptyLine(String line) {
    if (line == null) return true; // treat null as empty for safety
    return EMPTY_LINE_PATTERN.matcher(line).matches();
  }
}
