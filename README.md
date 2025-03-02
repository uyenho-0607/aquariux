# Automation Testing Framework

## Overview

This framework is designed using the **Page Object Model (POM)** design pattern, leveraging **Pytest and Playwright** to automate testing for **WEB** application

## Features
- **Faster execution** by using Playwright (compared to Selenium)
- **Headless execution** support for faster test execution
- Generates **detailed logs and reports** using **Allure report**
- Modular and scalable test structure following **POM design pattern**

## Installation

Clone the repository:

```bash
git clone https://github.com/uyenho-0607/aquariux.git
```

## Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

## Install Dependencies

```bash
pip3 install -r requirements.txt
```

## Configuration

Stored at `config/*.yaml` file

## Running Tests

### **Run Sample Test Suite (Default: Web)**
```bash
pytest tests/trade_page/
```
or sample test case
```bash
pytest test_01_place_buy_market_with_sl_and_tp.py
```

### **Run All Tests**
```bash
pytest tests/ 
```

### **Run in Headless Mode**
```bash
pytest --headless ...
```

## Allure report Sample
Please refer to *./allure_report_sample/*
