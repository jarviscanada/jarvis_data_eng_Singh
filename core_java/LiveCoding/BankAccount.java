import java.util.*;
import java.util.stream.Collectors;

public class BankAccount {
    private String accountNumber;
    private String ownerName;
    private double balance;
    private List<Double> transactions; 

    public BankAccount(String accountNumber, String ownerName, double startingBalance) {
        // Comprehensive input validation
        if (accountNumber == null || accountNumber.trim().isEmpty()) {
            throw new IllegalArgumentException("Account number cannot be null or empty");
        }
        if (ownerName == null || ownerName.trim().isEmpty()) {
            throw new IllegalArgumentException("Owner name cannot be null or empty");
        }
        if (startingBalance < 0) {
            throw new IllegalArgumentException("Starting balance cannot be negative. Provided: " + startingBalance);
        }
        if (Double.isNaN(startingBalance) || Double.isInfinite(startingBalance)) {
            throw new IllegalArgumentException("Starting balance must be a valid number");
        }
        
        this.accountNumber = accountNumber.trim();
        this.ownerName = ownerName.trim();
        this.balance = startingBalance;
        this.transactions = new ArrayList<>();
    }

    public void deposit(double amount) {
        // Input validation
        if (Double.isNaN(amount) || Double.isInfinite(amount)) {
            throw new IllegalArgumentException("Deposit amount must be a valid number");
        }
        if (amount <= 0) {
            throw new IllegalArgumentException("Deposit amount must be greater than 0. Provided: " + amount);
        }
        
        balance += amount;
        transactions.add(amount);
        System.out.println("? Deposited: $" + amount + " | New balance: $" + String.format("%.2f", balance));
    }

    public void withdraw(double amount) {
        // Input validation
        if (Double.isNaN(amount) || Double.isInfinite(amount)) {
            throw new IllegalArgumentException("Withdraw amount must be a valid number");
        }
        if (amount <= 0) {
            throw new IllegalArgumentException("Withdraw amount must be greater than 0. Provided: " + amount);
        }
        if (amount > balance) {
            throw new IllegalArgumentException(
                String.format("Insufficient funds. Requested: $%.2f | Available: $%.2f", amount, balance)
            );
        }
        
        balance -= amount;
        transactions.add(-amount);
        System.out.println("? Withdrawn: $" + amount + " | New balance: $" + String.format("%.2f", balance));
    }

    public double getBalance() {
        return balance;
    }

    public String getAccountInfo() {
        return String.format("Account: %s\nOwner: %s\nBalance: %.2f", accountNumber, ownerName, balance);
    }

    // using stream
    public double getTotalDeposited() {
        return transactions.stream()
                .filter(t -> t > 0)
                .mapToDouble(Double::doubleValue)
                .sum();
    }

    // using stream
    public double getTotalWithdrawn() {
        return transactions.stream()
                .filter(t -> t < 0)
                .mapToDouble(t -> Math.abs(t)) 
                .sum();
    }

    // using stream
    public double getLargestTransaction() {
        return transactions.stream()
                .mapToDouble(Math::abs)
                .max()
                .orElse(0.0);
    }

    public List<Double> getDeposits() {
        return transactions.stream()
                .filter(t -> t > 0)
                .collect(Collectors.toList());
    }
}   
