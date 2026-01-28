LS# MoMo SMS Data Processing System

## Project Overview

Week 1:
This project is an enterprise-level fullstack application designed to process Mobile Money (MoMo) SMS transaction data in XML format. The system performs data cleaning, categorization, storage in a relational database, and provides a comprehensive frontend interface for data analysis and visualization.

Week 2:
Your MoMo SMS data processing system needs to handle various types of mobile money transactions. From analyzing theXML data structure and business requirements, you need to design a database that can efficiently store, query, and analyze transaction data while maintaining data integrity and supporting future scalability.

## Team Information

## Team Name: EWD_Group2

**Team Members:**
- Jean Nepo Munezero
- Eric Hategekimana
- Alieu O Jobe
- Kouame Moaye Morel Yohan
- Frank Nkurunziza

## Project Objectives

Week 1:
The primary objective of this continuous formative assessment is to demonstrate proficiency in designing and developing an enterprise-level fullstack application with the following capabilities:

- Process Mobile Money SMS data in XML format
- Clean and categorize transaction data
- Store processed data in a relational database
- Build an intuitive frontend interface for data analysis
- Implement data visualization features
- Apply collaborative development workflows using Agile practices

Week 2:
Building on your team setup from Week 1, you will now design and implement the database foundation for your MoMo SMS data processing system. This assignment focuses on translating business requirements into a robust database schema and implementing it using SQL, while practicing data serialization concepts with JSON.
## System Architecture

Week 1:
The application follows a modern three-tier architecture:

1. **Data Layer (ETL)** - Extract, Transform, Load operations for XML data processing
2. **Backend Layer (API)** - RESTful API services for data management
3. **Frontend Layer (Web)** - User interface for data visualization and analysis

View the detailed system architecture diagram: [Architecture Diagram](https://app.diagrams.net/?src=about#G1JLxwy9hl4DwOZYv98llMVIHr4euuego0#%7B%22pageId%22%3A%22GxqXyq6CJ7gisuevURrI%22%7D)


## Project Structure

Week 1:
```
Team_Setup_and_Project_Planning/
│
├── actions/              # GitHub Actions workflow configurations
│
├── api/                  # Backend API service layer
│   ├── app.py           # Main application server
│   ├── db.py            # Database connection and queries
│   └── schemas.py       # Data models and validation
│
├── data/                 # Data storage
│   ├── processed/       # Processed data files
│   │   └── dashboard.json
│   ├── raw/             # Raw XML source files
│   │   └── momo_file.xml
│   └── db.sqlite3       # SQLite database
│
├── etl/                  # Extract, Transform, Load pipeline
│   ├── parse_xml.py     # XML parsing module
│   ├── clean_normalize.py  # Data cleaning and normalization
│   ├── categorize.py    # Transaction categorization
│   └── load_db.py       # Database loading module
│
├── web/                  # Frontend application
│   ├── index.html       # Main HTML page
│   ├── js/              # JavaScript files
│   └── style.css        # CSS styling
│
├── .env.example          # Environment variable template
├── .gitignore           # Git ignore rules
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```


3. JSON Data Models
File: examples/json_schemas.json
Includes:
One JSON object per entity (user, sms, transaction)
One complex JSON object representing a complete transaction with nested user + sms info
Used to demonstrate how data is serialized in API responses

Week 2:

Team_Setup_and_Project_Planning/
│
├── docs/
|    ├── erd_diagram.
|
├── database/
|    ├── database_setup.sql
|
|
├── examples/
│   ├── customer.json
│   ├── transaction_category.json
│   ├── system_log.json
│   ├── Transactions.json
│   └── complete_transaction.json
|
|
|
├── actions/              # GitHub Actions workflow configurations
│
├── api/                  # Backend API service layer
│   ├── app.py           # Main application server
│   ├── db.py            # Database connection and queries
│   └── schemas.py       # Data models and validation
│
├── data/                 # Data storage
│   ├── processed/       # Processed data files
│   │   └── dashboard.json
│   ├── raw/             # Raw XML source files
│   │   └── momo_file.xml
│   └── db.sqlite3       # SQLite database
│
├── etl/                  # Extract, Transform, Load pipeline
│   ├── parse_xml.py     # XML parsing module
│   ├── clean_normalize.py  # Data cleaning and normalization
│   ├── categorize.py    # Transaction categorization
│   └── load_db.py       # Database loading module
│
├── web/                  # Frontend application
│   ├── index.html       # Main HTML page
│   ├── js/              # JavaScript files
│   └── style.css        # CSS styling
│
├── .env.example          # Environment variable template
├── .gitignore           # Git ignore rules
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation

### Scrum Board

Week 1 & Week 2:
Access our project management board: [Trello Scrum Board](https://trello.com/invite/b/696677801090ad1325ce602d/ATTI3bedcb7f7813ee570f9fec3a1be0b6fcF601691B/teamsetupandprojectplanning)


- Course instructors for guidance and requirements
- Team members for collaboration and dedication
- Open-source community for tools and libraries

---

# DATABASE DOCUMENTATION

## Database Purpose

This database stores processed XML data in a structured, easily accessible format. It includes active tables for current operations and reserved tables (such as user_relationship) prepared for future feature development, ensuring the system can scale and evolve without requiring major architectural changes.

## Key Features

Transforms hierarchical XML data into optimized relational structures
Separates active tables from future-reserved tables for clear schema organization
Designed for extensibility and backward compatibility





**Last Updated:** January 2026  
**Version:** 1.0.0  
**Status:** In Development



