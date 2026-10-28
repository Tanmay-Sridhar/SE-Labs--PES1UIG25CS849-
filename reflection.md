# Lab 5 — Static Code Analysis: Reflection

*The questions below are suggested reflection questions, not verified questions from the lecturer.*

## 1. What is static code analysis, and why is it important?

Static code analysis is the process of examining source code without executing the program. It helps identify potential bugs, security vulnerabilities, and coding-style violations. In this lab, Pylint, Bandit, and Flake8 helped improve the quality, security, readability, and maintainability of the Python program.

## 2. What issues did you identify and fix during the lab?

I identified several issues, including a class-capacity bug, a mutable default argument, an overly broad exception handler, unsafe shell-command execution, invalid input handling, and file-handling problems. I corrected these issues to make the booking system more reliable and secure while preserving its intended functionality.

## 3. What are the differences between Pylint, Bandit, and Flake8?

Pylint checks overall code quality, naming conventions, documentation, and potential programming mistakes. Bandit identifies common security vulnerabilities in Python code, such as unsafe shell-command execution. Flake8 checks Python style and formatting, including indentation, whitespace, and line length. Using all three tools provides a more comprehensive analysis than relying on just one.

## 4. What did you learn from this lab?

I learned that code can appear to work correctly while still containing logical errors and security risks. Static analysis tools help identify these problems early, making code easier to maintain and safer to use. I also learned the importance of validating user input, handling exceptions appropriately, following coding standards, and rerunning analysis tools after fixing issues.
