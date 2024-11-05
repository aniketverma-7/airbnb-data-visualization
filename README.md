<img width="1705" alt="dashboard" src="https://github.com/user-attachments/assets/fc644e33-6b11-4072-9b62-fe3cd53ed6fa">

# Airbnb Insights in New York City

This project is a **Dash web application** that provides insights into Airbnb listings across New York City. The application allows users to explore and visualize Airbnb data through interactive features such as:

- **Interactive Map**: View the distribution of Airbnb listings across different boroughs.
- **Price Distribution Histogram**: Visualize listings by price range and borough.
- **Filterable Table**: Explore detailed information on Airbnb listings with sortable and searchable options.

## Features

### 1. **Interactive Map**
   - Displays a scatter plot map of Airbnb listings across New York City.
   - Hover over markers to see details about each listing, including:
     - Borough
     - Price
     - Room type
     - Number of reviews

### 2. **Filtering Options**
   - Users can filter listings by:
     - Borough
     - Price range
     - Room type
   - Filters update both the map and the table, allowing for a customized view of the data.

### 3. **Price Distribution Histogram**
   - A bar chart that shows the number of Airbnb listings by price range and borough.
   - Error bars represent variability in the price distributions across neighborhoods.

### 4. **Listings Table**
   - A sortable and searchable table that displays key information about Airbnb listings, including:
     - Listing name
     - Host details
     - Location
     - Cancellation policy
     - Room type
     - Price and service fee

## How to Run the Application

1. **Clone the repository:**
   ```bash
   git clone <repository-url>


## How to Run the Application

```bash
# Clone the repository to your local machine
git clone https://github.com/aniketverma-7/airbnb-data-visualization
```

# Change into the project directory
```bash
cd airbnb-data-visualization
```
# Create a virtual environment to manage dependencies
```bash
python3 -m venv <name of your env>
```

# Activate the virtual environment (use the appropriate command for your OS)
```bash
source env/bin/activate  # For Linux/Mac
```
```bash
.\env\Scripts\activate   # For Windows
```
# Install the required dependencies from the requirements file
```bash pip install -r requirements.txt```

# Run the Dash application
```bash python main.py```
