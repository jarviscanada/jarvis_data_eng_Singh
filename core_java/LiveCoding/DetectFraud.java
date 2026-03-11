import java.util.*;
import java.util.stream.Collectors;

public class DetectFraud {
    // Basic version using loop
    public static List<Integer> detectFraud(List<Integer> transactions, int threshold) {
        // Input validation
        if (transactions == null) {
            throw new IllegalArgumentException("Transactions list cannot be null");
        }
        if (transactions.isEmpty()) {
            throw new IllegalArgumentException("Transactions list cannot be empty");
        }
        if (threshold < 0) {
            throw new IllegalArgumentException("Threshold cannot be negative");
        }
        
        List<Integer> result = new ArrayList<>();
        for (Integer t : transactions) {
            if (t == null) {
                throw new IllegalArgumentException("Transaction value cannot be null");
            }
            if (t > threshold) {
                result.add(t);
            }
        }
        return result;
    }

    //Stream API
    public static List<Integer> detectFraudWithStream(List<Integer> transactions, int threshold) {
        // Input validation
        if (transactions == null) {
            throw new IllegalArgumentException("Transactions list cannot be null");
        }
        if (transactions.isEmpty()) {
            throw new IllegalArgumentException("Transactions list cannot be empty");
        }
        if (threshold < 0) {
            throw new IllegalArgumentException("Threshold cannot be negative");
        }
        
        return transactions.stream()
                .peek(t -> {
                    if (t == null) {
                        throw new IllegalArgumentException("Transaction value cannot be null");
                    }
                })
                .filter(t -> t > threshold)
                .collect(Collectors.toList());
    }
}
