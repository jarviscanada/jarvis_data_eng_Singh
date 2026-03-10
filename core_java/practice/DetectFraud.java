import java.util.*;
import java.util.stream.Collectors;

public class DetectFraud {
    // Basic version using loop
    public static List<Integer> detectFraud(List<Integer> transactions, int threshold) {
        List<Integer> result = new ArrayList<>();
        for (Integer t : transactions) {
            if (t > threshold) {
                result.add(t);
            }
        }
        return result;
    }

    //Stream API
    public static List<Integer> detectFraudWithStream(List<Integer> transactions, int threshold) {
        return transactions.stream()
                .filter(t -> t > threshold)
                .collect(Collectors.toList());
    }
}