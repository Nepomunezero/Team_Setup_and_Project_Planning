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
```
Team_Setup_and_Project_Planning/
│
├── docs/                           # Documentation files
│   └── erd_diagram.*               # Entity Relationship Diagram
│
├── database/                       # Database configurations
│   └── database_setup.sql          # Database schema and setup scripts
│
├── examples/                       # Sample data files
│   ├── customer.json               # Customer data example
│   ├── transaction_category.json  # Transaction category mappings
│   ├── system_log.json             # System log format example
│   ├── Transactions.json           # Transaction data example
│   └── complete_transaction.json   # Complete transaction record example
│
├── actions/                        # GitHub Actions workflow configurations
│
├── api/                            # Backend API service layer
│   ├── app.py                      # Main application server
│   ├── db.py                       # Database connection and queries
│   └── schemas.py                  # Data models and validation
│
├── data/                           # Data storage
│   ├── processed/                  # Processed data files
│   │   └── dashboard.json          # Dashboard data output
│   ├── raw/                        # Raw XML source files
│   │   └── momo_file.xml           # Mobile money transaction XML
│   └── db.sqlite3                  # SQLite database
│
├── etl/                            # Extract, Transform, Load pipeline
│   ├── parse_xml.py                # XML parsing module
│   ├── clean_normalize.py          # Data cleaning and normalization
│   ├── categorize.py               # Transaction categorization
│   └── load_db.py                  # Database loading module
│
├── web/                            # Frontend application
│   ├── index.html                  # Main HTML page
│   ├── js/                         # JavaScript files
│   └── style.css                   # CSS styling
│
├── .env.example                    # Environment variable template
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```
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




## Building and Securing a REST API

# TEAM TASK SHEET: https://docs.google.com/spreadsheets/d/1cmtYrJtk83bS9oa_knN8BFvS5o_fETDS4vIIqRpPwdE/edit?usp=sharing

A REST API for managing mobile money SMS transaction data, built with Python's http.server module. Demonstrates CRUD operations, authentication, data structures and algorithms, and API documentation.

## Features

- CRUD Operations: Create, Read, Update, Delete transactions
- Authentication: Basic Authentication with username/password
- Data Parsing: XML to JSON conversion with regex extraction
- Search Algorithms: Linear search vs Dictionary lookup comparison
- Query Filters: Filter transactions by type, amount, sender, recipient
- Comprehensive Documentation: Detailed API docs with examples
- Automated Testing: Python test suite and curl scripts
- Error Handling: Proper HTTP status codes and error messages

## Project Structure

```
rest_api_project/
├── api/
│   └── server.py
├── dsa/
│   ├── xml_parser.py
│   └── search_algorithms.py
├── docs/
│   └── api_docs.md
├── tests/
│   ├── test_api.py
│   └── curl_tests.sh
├── screenshots/
├── modified_sms_v2.xml
├── README.md
├── requirements.txt
└── IMPLEMENTATION_GUIDE.md
```

## Requirements

- Python 3.7 or higher
- requests library (for testing)
- Standard library modules (xml.etree.ElementTree, http.server, json, base64)

## Installation & Setup

Clone the repository:
```bash
git clone https://github.com/your-team/rest-api-project.git
cd rest-api-project
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Verify XML data file exists:
```bash
ls -l modified_sms_v2.xml
```

## Running the API

Start the server:
```bash
cd api
python server.py ../modified_sms_v2.xml
```

Custom port:
```bash
python server.py ../modified_sms_v2.xml 8080
```

The server runs at http://localhost:8000 with credentials:
- Username: admin
- Password: password123

## Testing

Automated testing:
```bash
cd tests
python test_api.py
```

Manual testing with curl:
```bash
cd tests
chmod +x curl_tests.sh
./curl_tests.sh
```

Testing with Postman:
1. Set Base URL: http://localhost:8000
2. Configure Basic Auth with admin/password123
3. Test endpoints per docs/api_docs.md

## API Documentation

Complete documentation available in docs/api_docs.md.

**Base URL:** http://localhost:8000

**Authentication:** Basic Auth (admin/password123)

**Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /transactions | List all transactions |
| GET | /transactions/{id} | Get specific transaction |
| POST | /transactions | Create new transaction |
| PUT | /transactions/{id} | Update transaction |
| DELETE | /transactions/{id} | Delete transaction |

**Example:**
```bash
curl -u admin:password123 http://localhost:8000/transactions
```

## Data Structures & Algorithms

Run DSA analysis:
```bash
cd dsa
python search_algorithms.py ../modified_sms_v2.xml
```

This compares:
- Linear Search: O(n) - Sequential checking
- Dictionary Lookup: O(1) - Hash table access
- Binary Search: O(log n) - Sorted array search

Dictionary lookup is significantly faster but uses more memory. See IMPLEMENTATION_GUIDE.md for detailed analysis.

## Security

Basic Authentication is used for educational purposes only. Limitations include:
- Credentials only base64-encoded
- No expiration
- Hardcoded values
- No rate limiting

Production recommendations:
- Use HTTPS
- Implement JWT tokens
- Use OAuth 2.0
- Store credentials in environment variables
- Hash passwords with bcrypt
- Add rate limiting
- Use API keys

## Assignment Requirements

All requirements fulfilled:
- Data Parsing: XML to JSON with regex extraction
- API Implementation: All CRUD endpoints functional
- Authentication: Basic Auth implemented
- API Documentation: Complete with examples
- DSA Integration: Linear search vs Dictionary comparison
- Testing: Automated tests and curl scripts
- Team Participation: Sheet included

## Troubleshooting

**Server won't start:**
```bash
lsof -i :8000
kill -9 <PID>
python server.py ../modified_sms_v2.xml 8080
```

**XML file not found:**
```bash
ls -l ../modified_sms_v2.xml
python server.py /full/path/to/modified_sms_v2.xml
```

**Authentication not working:**
```bash
curl -u admin:password123 -v http://localhost:8000/transactions
```

**Tests failing:**
Ensure server is running in separate terminal before running tests.

## Additional Resources

- Python http.server: https://docs.python.org/3/library/http.server.html
- Regular Expressions: https://regex101.com/
- REST API Design: https://restfulapi.net/
- Postman: https://www.postman.com/downloads/
- curl Documentation: https://curl.se/docs/

---

**Last Updated:** February 2, 2026
  
**Version:** 1.0.0







