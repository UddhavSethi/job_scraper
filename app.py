from flask import Flask, render_template, request, jsonify
from jobScraperv2 import scrape_linkedin_jobs

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
        results = scrape_linkedin_jobs(keyword=title, experience=experience, max_jobs=int(max_jobs))
        # Normalize keys for frontend
        jobs = [
            {
                'company': item.get('Company') or item.get('company') or '',
                'link': item.get('Link') or item.get('link') or ''
            }
            for item in results
        ]
        return jsonify({'jobs': jobs, 'title': title, 'experience': experience})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)