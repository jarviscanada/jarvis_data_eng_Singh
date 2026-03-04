package ca.jrvs.apps.practice;

public class RegexExcMain {
  public static void main(String[] args) {
    RegexExc r = new RegexExcImp();

    System.out.println(r.matchJpeg("a.jpg"));          // true
    System.out.println(r.matchJpeg("a.JPEG"));         // true
    System.out.println(r.matchJpeg("a.png"));          // false

    System.out.println(r.matchIp("0.0.0.0"));          // true
    System.out.println(r.matchIp("999.999.999.999"));  // true
    System.out.println(r.matchIp("1000.1.1.1"));       // false (doesn't match 1-3 digits)
    System.out.println(r.matchIp("1.1.1"));            // false

    System.out.println(r.isEmptyLine(""));             // true
    System.out.println(r.isEmptyLine("   \t"));        // true
    System.out.println(r.isEmptyLine("hello"));        // false
  }
}
