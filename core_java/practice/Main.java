import java.util.*;

public class Main {

    public static void main(String[] args) {
        try {
            // Test Detect Fraud
            List<Integer> transactions = Arrays.asList(20, 40, 5000, 30);
            int threshold = 1000;
            List<Integer> frauds = DetectFraud.detectFraud(transactions, threshold);
            System.out.println("Fraudulent transactions: " + frauds); // Expected: [5000]

            // Test Bank Acc
            BankAccount account = new BankAccount("12345", "Alice", 100.0);
            account.deposit(50.0);
            account.withdraw(30.0);
            System.out.println(account.getAccountInfo());
            

            // Stream API 
            System.out.println("Total deposited (stream): " + account.getTotalDeposited());
            System.out.println("Total withdrawn (stream): " + account.getTotalWithdrawn());
            System.out.println("Largest transaction (stream): " + account.getLargestTransaction());
            System.out.println("List of all deposits (stream): " + account.getDeposits());
        } catch (IllegalArgumentException iae) {
            System.err.println("Input error: " + iae.getMessage());
        } catch (Exception e) {
            System.err.println("Unexpected error: " + e);
            e.printStackTrace();
        }
    }
}