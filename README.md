# Job Scraper Web Application

A Flask-based web application that scrapes job listings from LinkedIn based on user input.

## Features

- Web interface for job searching
- LinkedIn job scraping with experience level filtering
- Modern, responsive UI
- Real-time job results

## Deployment on Render

### Option 1: Using Docker (Recommended)

1. Fork or clone this repository
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" and select "Web Service"
4. Connect your GitHub repository
5. Configure the service:
   - **Name**: `job-scraper-app`
   - **Environment**: `Docker`
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Build Command**: Leave empty (Dockerfile handles this)
   - **Start Command**: Leave empty (Dockerfile handles this)

6. Click "Create Web Service"

### Option 2: Using Python Environment

1. Fork or clone this repository
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" and select "Web Service"
4. Connect your GitHub repository
5. Configure the service:
   - **Name**: `job-scraper-app`
   - **Environment**: `Python 3`
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

6. Add environment variables:
   - `PYTHON_VERSION`: `3.11.0`

7. Click "Create Web Service"

## Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open http://localhost:5000 in your browser

## Troubleshooting

### "Failed to fetch" Error

If you encounter "Failed to fetch" errors on Render:

1. **Check the logs**: Go to your Render dashboard and check the service logs for errors
2. **Chrome installation**: The app requires Chrome to be installed. The Dockerfile handles this automatically
3. **Timeout issues**: The app limits job scraping to 30 jobs maximum to prevent timeouts
4. **Memory issues**: If you're on a free plan, consider upgrading to a paid plan for better performance

### Common Issues

1. **Chrome not found**: Make sure you're using the Docker deployment option
2. **Selenium errors**: The app includes fallback mechanisms for Selenium issues
3. **LinkedIn blocking**: The app uses undetected-chromedriver to avoid detection

## API Endpoints

- `GET /`: Main web interface
- `POST /api/jobs`: Job search API
- `GET /health`: Health check endpoint

## Environment Variables

- `PYTHON_VERSION`: Python version (default: 3.11.0)

## Dependencies

- Flask: Web framework
- Selenium: Web scraping
- undetected-chromedriver: Anti-detection Chrome driver
- pandas: Data manipulation
- gunicorn: WSGI server for production

## License

MIT License
