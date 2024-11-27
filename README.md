## Auction House Data Processor

### Description

This application processes auction house data from the **Throne and Liberty** game. It provides multiple features to generate reports and summaries based on API data, storing the results in a PostgreSQL database. Built using **Python**, **Flask**, and **SQLAlchemy**, this application serves as a web service that continuously fetches data and enables users to generate reports dynamically.

---

### Features

1. **Feature 1: Auction House Summary**
   - Fetches item data from the auction house API.
   - Generates an Excel file summarizing item details, including:
     - Name
     - Grade
     - Main Category
     - Subcategory
     - Sub-Subcategory (if applicable)
     - Trait IDs and their corresponding text values
     - Minimum Price
   - Allows selection of region via user input.

2. **Feature 2: Trait Analysis**
   - Applies to data where `Main Category` is `traitextract`.
   - Allows filtering by `Sub-Subcategory` to display:
     - Unique Trait IDs as rows.
     - Unique item names as columns.
     - Minimum prices corresponding to each Trait ID and item.
   - Items are sorted by grade, with higher grades listed first.
   - Column background colors are pastel-shaded based on the item's grade:
     - Grade 2: Green
     - Grade 3: Blue
     - Grade 4: Purple
     - Grade 5: Orange

3. **Continuous Data Fetching**
   - Regularly fetches item data from the API.
   - Stores the data in a PostgreSQL database for efficient access.

---

### Prerequisites

1. **Python** (version 3.8 or higher)
2. **PostgreSQL** (version 12 or higher)
3. Required Python libraries:
   - Flask
   - SQLAlchemy
   - Requests
   - Pandas
   - OpenPyXL
   - APScheduler
   - Psycopg2-Binary

---

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/auction-house-data-processor.git
   cd auction-house-data-processor
   ```

2. **Set Up PostgreSQL**
   - Install PostgreSQL:
     ```bash
     sudo apt update
     sudo apt install postgresql postgresql-contrib
     ```
   - Create a user and database:
     ```sql
     CREATE USER auction_user WITH PASSWORD 'your_password';
     CREATE DATABASE auction_house_db;
     GRANT ALL PRIVILEGES ON DATABASE auction_house_db TO auction_user;
     ```

3. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   - Set the PostgreSQL connection string in your environment:
     ```bash
     export DATABASE_URL="postgresql+psycopg2://auction_user:your_password@localhost/auction_house_db"
     ```

5. **Initialize the Database**
   ```bash
   python -c "from database import init_db; init_db()"
   ```

---

### Usage

1. **Start the Application**
   ```bash
   python app.py
   ```

2. **Access Features**
   - **Feature 1**: Generate Auction House Summary
     - Use the `/generate_summary` endpoint.
     - Example: Access `http://127.0.0.1:5000/generate_summary` in your browser.
   - **Feature 2**: Trait Analysis
     - Use the `/trait_analysis/<region>/<sub_sub_category>` endpoint.
     - Example: `http://127.0.0.1:5000/trait_analysis/as-f/Accessories`.

3. **View Generated Excel Files**
   - Files will be saved in the `output/` directory.

---

### File Structure

```
auction-house-data-processor/
│
├── app.py               # Flask web application
├── database.py          # Database models and initialization
├── features.py          # Feature implementations
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── output/              # Folder for generated Excel files
```

---

### Future Enhancements

- Add more features for analyzing auction house data.
- Implement user authentication for secure API access.
- Deploy the application on a cloud platform (e.g., AWS, Heroku).
- Add visualization for auction house trends.

---

### Contributing

1. Fork the repository.
2. Create a new feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add a meaningful message"
   ```
4. Push the changes and create a pull request.

---

### License

This project is licensed under the MIT License. See the `LICENSE` file for details. 

---

Feel free to reach out if you have any questions or suggestions!
