import java.util.*;
import java.util.stream.Collectors;

public class BankAccount {
    private String accountNumber;
    private String ownerName;
    private double balance;
    private List<Double> transactions; 

    public BankAccount(String accountNumber, String ownerName, double startingBalance) {
        if (startingBalance < 0) {
            throw new IllegalArgumentException("Starting balance cannot be negative");
        }
        this.accountNumber = accountNumber;
        this.ownerName = ownerName;
        this.balance = startingBalance;
        this.transactions = new ArrayList<>();
    }

    public void deposit(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Deposit amount must be greater than 0");
        }
        balance += amount;
        transactions.add(amount); 
    }

    public void withdraw(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Withdraw amount must be greater than 0");
        }
        if (amount > balance) {
            throw new IllegalArgumentException("Cannot withdraw more than current balance");
        }
        balance -= amount;
        transactions.add(-amount); 
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