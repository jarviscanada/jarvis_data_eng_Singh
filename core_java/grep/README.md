# Introduction

The grep application is a Java command-line program designed to recursively search files under a given root directory and match lines using a regular expression. It mimics the functionality of the Linux `grep` command. This project demonstrates core Java concepts such as file I/O, regex processing, lambda expressions, and streams. The application is built using Maven and packaged as a fat jar for dependency management. Docker is used to containerize the application for easy deployment and distribution.

# Quick Start

Build the project:

```bash
mvn clean package
```

# Run using fat jar
```bash
java -jar target/grep-1.0-SNAPSHOT.jar ".*Romeo.*Juliet.*" ./data ./out/grep.out
```

# Run using Docker
```bash
docker run --rm \
-v "$(pwd)/data:/data" \
-v "$(pwd)/out:/log" \
<docker_user>/grep ".*Romeo.*Juliet.*" /data /log/grep.out
```

# Verify output
```bash
cat ./out/grep.out
```

# Implementation

##Pseudocode
```bash
process():
  matchedLines = []

  for each file in listFiles(rootPath):
    for each line in readLines(file):
      if containsPattern(line):
        matchedLines.add(line)

  writeToFile(matchedLines)
```

# Performance Issue

The initial implementation loads file contents and matched lines into memory using lists. This design can cause memory issues when processing large files such as 50GB inputs. A better solution is to read input line by line using BufferedReader or Java Streams and write matches directly to the output file, which greatly reduces heap memory usage.

# Test

The application was tested manually using the sample Shakespeare text files in the data directory. I ran the Java grep app with the same regex used in Linux egrep -r and compared the outputs to verify correctness. I also tested the fat jar execution and Dockerized execution to ensure the application worked consistently across different runtime environments.

# Deployment

The application was packaged as a fat jar using the Maven Shade Plugin so that all dependencies were bundled into a single executable jar. It was then dockerized using a lightweight Java runtime image. The Docker container runs the jar file with java -jar, allowing the grep app to be distributed and executed easily without additional dependency setup on the host system.

# Improvement

1. Refactor the grep implementation to process files line by line instead of storing all lines in memory.
2. Add JUnit test cases for grep, regex, and lambda/stream implementations.
3. Improve Docker and Maven automation with CI/CD and versioned image tagging.
