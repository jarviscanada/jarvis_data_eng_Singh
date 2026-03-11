import java.util.*;

public class Main {

    public static void main(String[] args) {
        System.out.println("=== LIVE CODING: Fraud Detection & Bank Account ===");
        System.out.println();
        
        // Test 1: Detect Fraud
        testDetectFraud();
        System.out.println();
        
        // Test 2: Bank Account
        testBankAccount();
        System.out.println();
        
        // Test 3: Edge cases
        testEdgeCases();
    }
    
    private static void testDetectFraud() {
        System.out.println("--- TEST 1: Detect Fraud ---");
        try {
            List<Integer> transactions = Arrays.asList(20, 40, 5000, 30);
            int threshold = 1000;
            
            System.out.println("Transactions: " + transactions);
            System.out.println("Threshold: " + threshold);
            
            List<Integer> frauds = DetectFraud.detectFraud(transactions, threshold);
            System.out.println("? Fraudulent transactions: " + frauds);
        } catch (IllegalArgumentException e) {
            System.err.println("? Fraud Detection Error: " + e.getMessage());
        }
    }
    
    private static void testBankAccount() {
        System.out.println("--- TEST 2: Bank Account Operations ---");
        try {
            BankAccount account = new BankAccount("12345", "Alice", 100.0);
            System.out.println("? Account created");
            
            account.deposit(50.0);
            account.withdraw(30.0);
            
            System.out.println();
            System.out.println(account.getAccountInfo());
            System.out.println();
            
            // Stream API
            System.out.println("--- Stream API Analysis ---");
            System.out.println("Total deposited: $" + String.format("%.2f", account.getTotalDeposited()));
            System.out.println("Total withdrawn: $" + String.format("%.2f", account.getTotalWithdrawn()));
            System.out.println("Largest transaction: $" + String.format("%.2f", account.getLargestTransaction()));
            System.out.println("All deposits: " + account.getDeposits());
        } catch (IllegalArgumentException e) {
            System.err.println("? Bank Account Error: " + e.getMessage());
        }
    }
    
    private static void testEdgeCases() {
        System.out.println("--- TEST 3: Edge Cases & Error Handling ---");
        
        // Invalid account creation
        System.out.println("1. Creating account with null name:");
        try {
            BankAccount account = new BankAccount("123", null, 100.0);
        } catch (IllegalArgumentException e) {
            System.out.println("? Caught error: " + e.getMessage());
        }
        
        // Invalid deposit
        System.out.println("\n2. Attempting negative deposit:");
        try {
            BankAccount account = new BankAccount("456", "Bob", 100.0);
            account.deposit(-50.0);
        } catch (IllegalArgumentException e) {
            System.out.println("? Caught error: " + e.getMessage());
        }
        
        // Insufficient funds
        System.out.println("\n3. Attempting withdrawal exceeding balance:");
        try {
            BankAccount account = new BankAccount("789", "Charlie", 50.0);
            account.withdraw(100.0);
        } catch (IllegalArgumentException e) {
            System.out.println("? Caught error: " + e.getMessage());
        }
        
        // Null transaction list
        System.out.println("\n4. Detecting fraud with null transaction list:");
        try {
            DetectFraud.detectFraud(null, 1000);
        } catch (IllegalArgumentException e) {
            System.out.println("? Caught error: " + e.getMessage());
        }
    }
}
