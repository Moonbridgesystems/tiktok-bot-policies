"""
Flask Dashboard for TikTok Viral Clothing Bot
"""
from flask import Flask, render_template, jsonify, request
from bot.database import Database
import config

app = Flask(__name__)
db = Database()


@app.route('/')
def index():
    """Render main dashboard page"""
    return render_template('index.html')


@app.route('/api/videos')
def get_videos():
    """
    API endpoint to get videos
    Query params:
        - sort_by: Column to sort by (default: product_inquiry_comments)
        - order: Sort order (default: DESC)
    """
    sort_by = request.args.get('sort_by', 'product_inquiry_comments')
    order = request.args.get('order', 'DESC')
    
    videos = db.get_all_videos(sort_by=sort_by, order=order)
    
    return jsonify({
        'success': True,
        'count': len(videos),
        'videos': videos
    })


@app.route('/api/stats')
def get_stats():
    """Get dashboard statistics"""
    videos = db.get_all_videos()
    
    total_videos = len(videos)
    total_inquiries = sum(v.get('product_inquiry_comments', 0) for v in videos)
    total_views = sum(v.get('views', 0) for v in videos)
    total_likes = sum(v.get('likes', 0) for v in videos)
    
    return jsonify({
        'success': True,
        'stats': {
            'total_videos': total_videos,
            'total_inquiries': total_inquiries,
            'total_views': total_views,
            'total_likes': total_likes,
        }
    })


def run_dashboard():
    """Start the Flask dashboard"""
    print(f"Starting dashboard at http://{config.DASHBOARD_HOST}:{config.DASHBOARD_PORT}")
    app.run(
        host=config.DASHBOARD_HOST,
        port=config.DASHBOARD_PORT,
        debug=False
    )


if __name__ == '__main__':
    run_dashboard()
