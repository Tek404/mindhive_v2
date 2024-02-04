## Prerequisites:
- python 3.11.1
- node v20.11.0
- ChromeDriver for selenium (https://chromedriver.chromium.org/downloads)
1. Install the required dependencies
`pip install -r requirements.txt`
2. Include a .env file as follows in the outlet_backend directory to set the environment variables of the server:
    ```
    GOOGLE_MAPS_API_KEY="your-google-api-key"
    ```
3. Navigate to outlet_backend directory and run command below
`python manage.py migrate`
`python manage.py scrape_website`
`python manage.py runserver`
4. Navigate to map-visuals directory and run command below
`npm install`
`npm start`
