LS# MoMo SMS Data Processing System

## Project Overview

This project is an enterprise-level fullstack application designed to process Mobile Money (MoMo) SMS transaction data in XML format. The system performs data cleaning, categorization, storage in a relational database, and provides a comprehensive frontend interface for data analysis and visualization.

## Team Information

**Team Name:** EWD_Group2

**Team Members:**
- Jean Nepo Munezero
- Eric Hategekimana
- Alieu O Jobe
- Kouame Moaye Morel Yohan
- Frank Nkurunziza

## Project Objectives

The primary objective of this continuous formative assessment is to demonstrate proficiency in designing and developing an enterprise-level fullstack application with the following capabilities:

- Process Mobile Money SMS data in XML format
- Clean and categorize transaction data
- Store processed data in a relational database
- Build an intuitive frontend interface for data analysis
- Implement data visualization features
- Apply collaborative development workflows using Agile practices

## System Architecture

The application follows a modern three-tier architecture:

1. **Data Layer (ETL)** - Extract, Transform, Load operations for XML data processing
2. **Backend Layer (API)** - RESTful API services for data management
3. **Frontend Layer (Web)** - User interface for data visualization and analysis

View the detailed system architecture diagram: [Architecture Diagram](https://app.diagrams.net/?src=about#G1JLxwy9hl4DwOZYv98llMVIHr4euuego0#%7B%22pageId%22%3A%22GxqXyq6CJ7gisuevURrI%22%7D)

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      MoMo SMS Source (XML files)                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ETL Pipeline (Python)                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. parse_xml.py      - Reads raw XML files              │  │
│  │ 2. clean_normalize.py - Fix dates, standardize phones    │  │
│  │ 3. categorize.py      - Tag transaction types (Payment)  │  │
│  │ 4. load_db.py         - Save to SQLite database          │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                           Data Storage                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. processed/        - dashboard.json                    │  │
│  │ 2. raw/              - momo_file.xml                     │  │
│  │ 3. db.sqlite3        - SQLite database                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                        API Layer (Backend)                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • app.py             - Main application server           │  │
│  │ • db.py              - Database connection & queries     │  │
│  │ • schemas.py         - Data models & validation          │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Web Frontend (User Interface)               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • index.html         - Main web page                     │  │
│  │ • js/                - JavaScript functionality          │  │
│  │ • style.css          - Styling and layout                │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Project Structure

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

## Technology Stack

### Backend
- Python 3.8+ for ETL processing and data manipulation
- SQLite for relational database storage
- RESTful API framework for backend services
- XML parsing libraries for data extraction

### Frontend
- HTML5 for structure
- CSS3 for styling and responsive design
- JavaScript for interactive functionality
- Data visualization libraries for charts and graphs

### ETL Pipeline Components
- **parse_xml.py** - XML file parsing and data extraction
- **clean_normalize.py** - Data cleaning, date formatting, phone number standardization
- **categorize.py** - Transaction type classification (e.g., Payment, Transfer)
- **load_db.py** - Database insertion and management

## Getting Started

### Prerequisites

- Python 3.8 or higher
- SQLite (included with Python)
- Web browser (Chrome, Firefox, Safari, or Edge)
- Git for version control
- Text editor or IDE (VS Code, PyCharm, etc.)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Nepomunezero/Team_Setup_and_Project_Planning.git
cd Team_Setup_and_Project_Planning
```

2. Set up Python environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your database path and API configuration
```

4. Process XML data through ETL pipeline:
```bash
cd etl
python parse_xml.py
python clean_normalize.py
python categorize.py
python load_db.py
```

5. Start the backend API:
```bash
cd api
python app.py
```

6. Open the frontend:
```bash
cd web
# Open index.html in your web browser
# Or use a local server:
python -m http.server 8000
# Then navigate to http://localhost:8000
```

## Features

### ETL Pipeline
- **XML Parsing** - Extract transaction data from XML files
- **Data Cleaning** - Fix date formats and standardize data
- **Phone Standardization** - Normalize phone number formats
- **Transaction Categorization** - Classify transactions by type (Payment, Transfer, etc.)
- **Database Loading** - Store processed data in SQLite
- **Error Handling** - Robust error logging and validation

### Backend API
- RESTful endpoints for CRUD operations
- Database query management through db.py
- Data schema validation via schemas.py
- Transaction filtering and search
- JSON data export for dashboard
- Efficient data retrieval

### Frontend Interface
- Dashboard with key transaction metrics
- Transaction list with filtering options
- Interactive data visualizations
- Clean and responsive design
- Real-time data updates
- Export functionality

## Development Workflow

This project follows Agile methodology using Scrum framework:

- **Sprint Duration:** 1-2 weeks
- **Daily Standups:** Team synchronization meetings
- **Sprint Planning:** Task estimation and assignment
- **Sprint Review:** Demo and stakeholder feedback
- **Sprint Retrospective:** Continuous improvement

### Scrum Board

Access our project management board: [Trello Scrum Board](https://trello.com/invite/b/696677801090ad1325ce602d/ATTI3bedcb7f7813ee570f9fec3a1be0b6fcF601691B/teamsetupandprojectplanning)

## Contributing

### Branching Strategy

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - Individual feature branches
- `bugfix/*` - Bug fix branches

### Commit Message Convention

Follow conventional commits format:
```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Pull Request Process

1. Create a feature branch from `develop`
2. Implement changes with tests
3. Update documentation as needed
4. Submit pull request with clear description
5. Request code review from team members
6. Address review feedback
7. Merge after approval

## Testing

### Backend Tests
```bash
python -m pytest tests/
```

### Frontend Tests
```bash
cd web
# Open index.html in browser and test functionality manually
# Or use browser testing tools
```

## Data Flow

The application processes data through the following workflow:

1. **Data Source** - Raw XML files containing MoMo SMS transaction data
2. **ETL Pipeline** - Four-stage processing:
   - Parse XML files and extract transaction data
   - Clean and normalize dates and phone numbers
   - Categorize transactions by type
   - Load processed data into SQLite database
3. **Data Storage** - Three storage locations:
   - Raw XML files in `data/raw/`
   - Processed JSON in `data/processed/`
   - SQLite database as `data/db.sqlite3`
4. **API Layer** - Backend services provide data access
5. **Web Interface** - Frontend displays and visualizes data

## Deployment

### Backend Deployment
- Configure production environment variables
- Set up database connection
- Deploy to cloud platform (AWS/Azure/GCP)
- Configure SSL certificates
- Set up monitoring and logging

### Frontend Deployment
- Test locally by opening index.html in browser
- Deploy to hosting service (Netlify/Vercel/GitHub Pages)
- Upload web/ directory contents
- Configure custom domain if needed
- Ensure API endpoints are correctly configured

## API Documentation

API documentation is available at `/api/docs` when running the development server.

### Key Endpoints

- `GET /api/transactions` - Retrieve transactions
- `POST /api/transactions` - Create new transaction
- `GET /api/transactions/:id` - Get specific transaction
- `PUT /api/transactions/:id` - Update transaction
- `DELETE /api/transactions/:id` - Delete transaction
- `GET /api/analytics` - Get analytics data

## Data Schema

### Transaction Model
```
{
  "id": "string",
  "transaction_id": "string",
  "date": "datetime",
  "amount": "decimal",
  "type": "string",
  "category": "string",
  "sender": "string",
  "receiver": "string",
  "status": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Performance Considerations

- Database indexing for faster queries
- Caching layer for frequently accessed data
- Pagination for large datasets
- Asynchronous processing for heavy operations
- CDN for static asset delivery

## Security Measures

- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CSRF tokens
- Authentication middleware
- Rate limiting
- Encrypted data transmission (HTTPS)
- Secure credential storage

## Troubleshooting

### Common Issues

**Database Connection Error**
- Verify database credentials in `.env`
- Ensure database service is running
- Check network connectivity

**API Not Responding**
- Confirm API server is running on correct port
- Check app.py configuration
- Review error logs in console
- Verify database connection

**ETL Pipeline Errors**
- Ensure XML files are in `data/raw/` directory
- Check XML file format and structure
- Verify Python dependencies are installed
- Review ETL script logs for specific errors

**Frontend Not Loading**
- Check browser console for JavaScript errors
- Verify API endpoint URLs in JavaScript files
- Ensure all files are in correct directories
- Test with different browsers

## Roadmap

### Phase 1: Foundation (Week 1-2)
- Team setup and repository configuration
- System architecture design
- Development environment setup
- Basic project structure

### Phase 2: Backend Development (Week 3-4)
- Database schema design
- ETL pipeline implementation
- API endpoint development
- Testing and validation

### Phase 3: Frontend Development (Week 5-6)
- UI/UX design
- Component implementation
- Data visualization integration
- Responsive design

### Phase 4: Integration & Testing (Week 7)
- Frontend-backend integration
- End-to-end testing
- Performance optimization
- Bug fixes

### Phase 5: Deployment & Documentation (Week 8)
- Production deployment
- User documentation
- Code documentation
- Final presentation

## Learning Outcomes

This project demonstrates competency in:

- Fullstack application development
- XML data processing and ETL pipelines
- Database design and management
- RESTful API development
- Modern frontend frameworks
- Data visualization techniques
- Agile development practices
- Git workflow and collaboration
- Testing and quality assurance
- Deployment and DevOps

## License

This project is created for educational purposes as part of a continuous formative assessment.

## Support

For questions or issues, please contact team members or create an issue in the GitHub repository.

## Acknowledgments

- Course instructors for guidance and requirements
- Team members for collaboration and dedication
- Open-source community for tools and libraries

---

**Last Updated:** January 2026  
**Version:** 1.0.0  
**Status:** In Development
