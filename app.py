from flask import Flask, render_template, request, jsonify
from jobScraperv2 import scrape_linkedin_jobs
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/jobs', methods=['POST'])
def get_jobs():
    data = request.get_json(silent=True) or {}
    title = data.get('title')
    experience = data.get('experience')  # LinkedIn codes like "1,2"
    max_jobs = data.get('max_jobs', 20)

    if not title or not experience:
        return jsonify({'error': 'title and experience are required'}), 400

    try:
        logger.info(f"Starting job search for: {title} with experience: {experience}")
        
        # Limit max_jobs to prevent timeouts
        max_jobs = min(int(max_jobs), 30)
        
        results = scrape_linkedin_jobs(keyword=title, experience=experience, max_jobs=max_jobs)
        
        # Normalize keys for frontend
        jobs = [
            {
                'company': item.get('Company') or item.get('company') or 'Company',
                'link': item.get('Link') or item.get('link') or '#'
            }
            for item in results
        ]
        
        logger.info(f"Successfully found {len(jobs)} jobs")
        return jsonify({'jobs': jobs, 'title': title, 'experience': experience})
        
    except Exception as e:
        logger.error(f"Error during job scraping: {str(e)}")
        logger.error(traceback.format_exc())
        
        # Return a helpful error message
        error_message = "Unable to fetch jobs at the moment. Please try again later."
        return jsonify({'error': error_message}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for Render"""
    return jsonify({'status': 'healthy', 'message': 'Job scraper is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)