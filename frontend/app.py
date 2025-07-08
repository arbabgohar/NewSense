import streamlit as st
import requests
from datetime import datetime
from typing import List, Dict, Any

# Page configuration
st.set_page_config(
    page_title="NewsSense — News Digest",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean, minimal design
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        color: #1f1f1f;
        margin-bottom: 1rem;
    }
    .news-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: box-shadow 0.3s ease;
    }
    .news-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        cursor: pointer;
    }
    .headline {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f1f1f;
        margin-bottom: 0.5rem;
    }
    .summary {
        color: #4a4a4a;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    .meta {
        font-size: 0.85rem;
        color: #666;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .category-badge {
        background-color: #f0f2f6;
        color: #1f1f1f;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    .sidebar .sidebar-content {
        padding: 1rem;
    }
    @media (max-width: 768px) {
        .news-card {
            padding: 1rem;
        }
        .headline {
            font-size: 1.1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Categories configuration
CATEGORIES = {
    "All": "🌐",
    "Stock": "📈", 
    "Politics": "🏛️",
    "Tech": "💻",
    "Health": "🏥",
    "Sports": "⚽",
    "Entertainment": "🎬",
    "Science": "🔬"
}

def get_summaries(category: str) -> List[Dict[str, Any]]:
    """Fetch summaries from FastAPI backend"""
    try:
        url = f"http://localhost:8000/digest?category={category}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json().get("summaries", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch summaries: {e}")
        return []

def format_timestamp(timestamp: str) -> str:
    """Format timestamp for display"""
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except:
        return timestamp

def render_news_card(item: Dict[str, Any]) -> None:
    """Render a single news card with only the summary, no headline or emojis"""
    st.markdown(f"""
    <div class="news-card">
        <div class="summary">{item.get('summary', 'No summary available')}</div>
        <div class="meta">
            <span>📰 {item.get('source', 'Unknown source')}</span>
            <span>🕒 {format_timestamp(item.get('timestamp', 'Unknown time'))}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Main header
    st.markdown('<div class="main-header">📰 NewsSense — News Digest</div>', unsafe_allow_html=True)
    
    # Left sidebar for categories
    with st.sidebar:
        st.header("📂 Categories")
        st.markdown("---")
        
        # Category selection
        selected_category = st.selectbox(
            "Choose a category:",
            options=list(CATEGORIES.keys()),
            index=0,
            key="category_selector"
        )
        
        st.markdown("---")
        
        # Refresh button
        if st.button("🔄 Refresh News", type="primary", use_container_width=True):
            st.session_state.refresh_triggered = True
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        NewsSense provides AI-powered news summaries to help you stay informed with concise, easy-to-understand content.
        """)
    
    # Right area for news display
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Check if refresh was triggered or if it's the first load
        if st.session_state.get("refresh_triggered", False) or "initial_load" not in st.session_state:
            with st.spinner(f"Fetching {selected_category} news..."):
                summaries = get_summaries(selected_category)
                
                if summaries:
                    st.success(f"✅ Found {len(summaries)} news items for {selected_category}")
                    st.markdown("---")
                    
                    # Display news cards
                    for item in summaries:
                        render_news_card(item)
                        
                        # Optional: Add expander for future details
                        with st.expander("📋 More Details", expanded=False):
                            st.markdown(f"**URL:** [{item.get('url', 'No URL')}]({item.get('url', '#')})")
                            st.markdown(f"**Full Timestamp:** {item.get('timestamp', 'Unknown')}")
                            st.markdown(f"**Category:** {item.get('category', 'Unknown')}")
                            st.markdown(f"**Source:** {item.get('source', 'Unknown')}")
                else:
                    st.warning(f"No news available for {selected_category} category.")
                    st.info("Try selecting a different category or check if the backend is running.")
            
            # Reset refresh trigger
            st.session_state.refresh_triggered = False
            st.session_state.initial_load = True
        
        # Show initial message if no refresh triggered
        elif "initial_load" not in st.session_state:
            st.info("👈 Select a category from the sidebar and click 'Refresh News' to get started.")
            st.session_state.initial_load = True

if __name__ == "__main__":
    main() 