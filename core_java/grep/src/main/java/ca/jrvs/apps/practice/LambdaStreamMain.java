package ca.jrvs.apps.practice;

import java.util.Arrays;
import java.util.List;

public class LambdaStreamMain {

  public static void main(String[] args) {
    LambdaStreamExc exc = new LambdaStreamImp();

    System.out.println(exc.toList(exc.createStrStream("a", "b", "c")));
    System.out.println(exc.toList(exc.toUpperCase("java", "grep", "stream")));
    System.out.println(exc.toList(exc.filter(exc.createStrStream("java", "scala", "python"), "a")));
    System.out.println(exc.toList(exc.createIntStream(new int[]{1, 2, 3, 4, 5})));
    System.out.println(exc.toList(exc.createIntStream(0, 5)));
    System.out.println(exc.toList(exc.getOdd(exc.createIntStream(0, 10))));
    System.out.println(
        exc.squareRootIntStream(exc.createIntStream(new int[]{1, 4, 9, 16}))
            .boxed()
            .toList()
    );

    exc.printMessages(new String[]{"a", "b", "c"}, exc.getLambdaPrinter("msg:", "!"));
    exc.printOdd(exc.createIntStream(0, 5), exc.getLambdaPrinter("odd number:", "!"));

    List<Integer> a = Arrays.asList(1, 2);
    List<Integer> b = Arrays.asList(3, 4);
    System.out.println(exc.toList(exc.flatNestedInt(Arrays.asList(a, b).stream())));
  }
}
