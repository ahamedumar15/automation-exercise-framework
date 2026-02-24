#  E-Commerce Test Automation Framework

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Selenium](https://img.shields.io/badge/Selenium-4.16.0-green.svg)
![Pytest](https://img.shields.io/badge/Pytest-7.4.3-red.svg)
![Tests](https://img.shields.io/badge/Tests-40+-success.svg)
![Coverage](https://img.shields.io/badge/Coverage-85%25-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> **Test automation framework** built with Python, Selenium WebDriver, and pytest. Demonstrates enterprise-level QA engineering practices including Page Object Model design, CI/CD integration, and comprehensive test coverage.

**🔗 Live Application Under Test:** [automationexercise.com](https://automationexercise.com)



##  Overview

This project showcases a **comprehensive test automation solution** for an e-commerce platform, implementing industry best practices and modern automation techniques. The framework is designed to be scalable, maintainable, and production-ready.

### Project Highlights

- ✅ **30+ Automated Test Cases** covering critical user workflows
- ✅ **85%+ Test Coverage** of core application features
- ✅ **60% Faster Execution** through parallel testing
- ✅ **Multi-Browser Support** (Chrome, Firefox, Edge)
- ✅ **CI/CD Ready** with GitHub Actions
- ✅ **Zero Hard-Coded Waits** using intelligent wait strategies
- ✅ **Comprehensive Reporting** with HTML reports and screenshots

---

##  Key Features

### 🏗️ Architecture & Design

- **Page Object Model (POM)** - Clean separation of test logic and page elements
- **Modular Framework** - Reusable components and utilities
- **Factory Pattern** - Dynamic WebDriver instantiation
- **Data-Driven Testing** - Faker library for dynamic test data generation
- **Layered Architecture** - Config, Pages, Tests, Utilities separation

### 🧪 Testing Capabilities

- **Parallel Execution** - pytest-xdist for concurrent test execution
- **Cross-Browser Testing** - Chrome, Firefox, Edge support
- **Headless Mode** - CI/CD compatible headless execution
- **Smart Waits** - Explicit waits with custom conditions
- **Screenshot Capture** - Automatic screenshots on test failure
- **Detailed Logging** - Console and file logging with multiple levels

### 📊 Reporting & Analytics

- **HTML Reports** - Beautiful, interactive test reports
- **JUnit XML** - CI/CD tool integration
- **Test Metrics** - Execution time, pass/fail rates
- **Screenshot Evidence** - Visual proof of test failures
- **Comprehensive Logs** - Debug-friendly detailed logs

### 🔄 CI/CD Integration

- **GitHub Actions** - Automated testing on push/PR
- **Docker Support** - Containerized test execution


---

##  Test Coverage

### Functional Areas Tested

| Module | Test Cases | Coverage |
|--------|-----------|----------|
| **User Registration** | 4 | 90% |
| **Authentication** | 6 | 95% |
| **Product Browsing** | 8 | 85% |
| **Search Functionality** | 5 | 90% |
| **Shopping Cart** | 8 | 85% |
| **Edge Cases** | 14 | 80% |
| **Total** | **40+** | **85%+** |

### Test Scenarios

- ✅ User registration with valid/invalid data
- ✅ Login/logout functionality
- ✅ Password validation
- ✅ Product search (valid, empty, special characters)
- ✅ Product detail viewing
- ✅ Add to cart functionality
- ✅ Cart quantity management
- ✅ Remove from cart
- ✅ Category filtering
- ✅ Brand filtering
- ✅ Newsletter subscription
- ✅ Form validations
- ✅ Session persistence
- ✅ Negative testing scenarios

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager
- Chrome/Firefox browser

### Installation

```bash
# Clone repository
git clone https://github.com/ahamedumar15/automation-exercise-framework.git
cd automation-exercise-framework

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Tests

```bash
# Run all tests
pytest -v

# Run smoke tests only (quick validation)
pytest -m smoke -v

# Run with HTML report
pytest --html=reports/report.html --self-contained-html

# Run in parallel (faster execution)
pytest -n auto -v

# Run specific test file
pytest tests/test_login.py -v

# Run in headless mode
export HEADLESS=true
pytest -v
```

---

## 🎓 Skills Demonstrated

### Technical Skills

- ✅ **Python Programming** - OOP, modules, exception handling
- ✅ **Selenium WebDriver** - Element location, actions, waits, JavaScript execution
- ✅ **Test Automation** - Framework design, test case development
- ✅ **pytest Framework** - Fixtures, markers, plugins, parameterization
- ✅ **Page Object Model** - Design pattern implementation
- ✅ **CI/CD** - GitHub Actions

---

**This project demonstrates my ability to design, develop, and maintain production quality test automation solutions.**
