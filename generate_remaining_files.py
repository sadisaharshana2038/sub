#!/usr/bin/env python3
"""
Script to generate all remaining bot files
Ensures complete, production-ready code
"""

import os
from pathlib import Path

# All file contents as templates
FILES = {
    "indexer.py": '''"""
Channel indexer for auto-indexing subtitle files
Monitors source channel and indexes new files automatically
"""

import logging
import asyncio
from datetime import datetime
from pyrogram import Client
from pyrogram.types import Message
from database import Database
from utils import clean_filename, format_file_size, is_subtitle_file
from config import UPDATE_CHANNEL_ID

logger = logging.getLogger(__name__)


class ChannelIndexer:
    """Auto-indexer for channel subtitle files"""
    
    def __init__(self, app: Client, db: Database, channel_id: int):
        """Initialize indexer"""
        self.app = app
        self.db = db
        self.channel_id = channel_id
        self.running = False
        
    async def start(self):
        """Start monitoring channel"""
        try:
            self.running = True
            logger.info(f"Channel indexer started for channel {self.channel_id}")
            
            # Index existing files on startup
            await self.index_existing_files()
            
        except Exception as e:
            logger.error(f"Error starting indexer: {e}")
    
    async def stop(self):
        """Stop indexer"""
        self.running = False
        logger.info("Channel indexer stopped")
    
    async def index_existing_files(self, limit: int = 100):
        """Index existing files from channel history"""
        try:
            logger.info(f"Indexing existing files from channel {self.channel_id}...")
            
            indexed = 0
            async for message in self.app.get_chat_history(self.channel_id, limit=limit):
                if message.document:
                    if await self.process_file(message):
                        indexed += 1
            
            logger.info(f"Indexed {indexed} existing files")
            return indexed
            
        except Exception as e:
            logger.error(f"Error indexing existing files: {e}")
            return 0
    
    async def process_file(self, message: Message) -> bool:
        """Process and index a subtitle file"""
        try:
            document = message.document
            
            # Check if it\\'s a subtitle file
            if not is_subtitle_file(document.file_name):
                return False
            
            # Clean filename and extract metadata
            clean_title, year, quality = clean_filename(document.file_name)
            
            # Prepare file data
            file_data = {
                "file_id": document.file_id,
                "file_name": document.file_name,
                "file_size": document.file_size,
                "title": document.file_name.rsplit(\\'.\\', 1)[0],
                "clean_title": clean_title,
                "year": year,
                "quality": quality,
                "message_id": message.id,
                "channel_id": self.channel_id
            }
            
            # Add to database
            added = await self.db.add_file(file_data)
            
            if added:
                logger.info(f"Indexed new file: {clean_title}")
                
                # Send notification to update channel
                if UPDATE_CHANNEL_ID:
                    await self.send_update_notification(file_data)
                
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            return False
    
    async def send_update_notification(self, file_data: dict):
        """Send notification about new file to update channel"""
        try:
            notification = (
                "🆕 <b>New Subtitle Added!</b>\\\\n\\\\n"
                f"📁 <b>{file_data[\\'clean_title\\']}</b>\\\\n"
                f"📅 Year: {file_data[\\'year\\'] or \\'N/A\\'}\\\\n"
                f"🎬 Quality: {file_data[\\'quality\\'] or \\'N/A\\'}\\\\n"
                f"📦 Size: {format_file_size(file_data[\\'file_size\\'])}\\\\n\\\\n"
                "Search for it in the bot to download!"
            )
            
            await self.app.send_message(UPDATE_CHANNEL_ID, notification)
            
        except Exception as e:
            logger.error(f"Error sending update notification: {e}")
''',

    "tmdb_client.py": '''"""
TMDB API client for movie/TV show information
Used in request system to fetch movie details
"""

import logging
import aiohttp
from typing import List, Dict, Optional
from config import TMDB_API_KEY, TMDB_BASE_URL, TMDB_IMAGE_BASE
from utils import truncate_text

logger = logging.getLogger(__name__)


class TMDBClient:
    """The Movie Database API client"""
    
    def __init__(self):
        """Initialize TMDB client"""
        self.api_key = TMDB_API_KEY
        self.base_url = TMDB_BASE_URL
        self.image_base = TMDB_IMAGE_BASE
        self.session = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def search_multi(self, query: str) -> List[Dict]:
        """
        Search for movies and TV shows
        
        Args:
            query: Search query
        
        Returns:
            List of search results (max 10)
        """
        try:
            if not self.api_key:
                logger.warning("TMDB API key not configured")
                return []
            
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            url = f"{self.base_url}/search/multi"
            params = {
                "api_key": self.api_key,
                "query": query,
                "page": 1
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get("results", [])
                    
                    # Filter to movies and TV shows only
                    filtered = [
                        r for r in results 
                        if r.get("media_type") in ["movie", "tv"]
                    ]
                    
                    return filtered[:10]  # Return max 10 results
                else:
                    logger.error(f"TMDB API error: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error searching TMDB: {e}")
            return []
    
    async def get_movie_details(self, movie_id: int) -> Optional[Dict]:
        """
        Get detailed information about a movie
        
        Args:
            movie_id: TMDB movie ID
        
        Returns:
            Movie details dict or None
        """
        try:
            if not self.api_key or not self.session:
                return None
            
            url = f"{self.base_url}/movie/{movie_id}"
            params = {"api_key": self.api_key}
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._format_movie_details(data)
                return None
                
        except Exception as e:
            logger.error(f"Error getting movie details: {e}")
            return None
    
    async def get_tv_details(self, tv_id: int) -> Optional[Dict]:
        """
        Get detailed information about a TV show
        
        Args:
            tv_id: TMDB TV show ID
        
        Returns:
            TV show details dict or None
        """
        try:
            if not self.api_key or not self.session:
                return None
            
            url = f"{self.base_url}/tv/{tv_id}"
            params = {"api_key": self.api_key}
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._format_tv_details(data)
                return None
                
        except Exception as e:
            logger.error(f"Error getting TV details: {e}")
            return None
    
    def _format_movie_details(self, data: Dict) -> Dict:
        """Format movie data for display"""
        return {
            "tmdb_id": data.get("id"),
            "title": data.get("title", "Unknown"),
            "year": data.get("release_date", "")[:4] if data.get("release_date") else None,
            "rating": round(data.get("vote_average", 0), 1),
            "runtime": data.get("runtime", 0),
            "genres": ", ".join([g["name"] for g in data.get("genres", [])]),
            "overview": truncate_text(data.get("overview", "No description available"), 300),
            "poster_url": f"{self.image_base}{data.get(\\'poster_path\\')}" if data.get("poster_path") else None,
            "media_type": "movie"
        }
    
    def _format_tv_details(self, data: Dict) -> Dict:
        """Format TV show data for display"""
        return {
            "tmdb_id": data.get("id"),
            "title": data.get("name", "Unknown"),
            "year": data.get("first_air_date", "")[:4] if data.get("first_air_date") else None,
            "rating": round(data.get("vote_average", 0), 1),
            "runtime": data.get("episode_run_time", [0])[0] if data.get("episode_run_time") else 0,
            "genres": ", ".join([g["name"] for g in data.get("genres", [])]),
            "overview": truncate_text(data.get("overview", "No description available"), 300),
            "poster_url": f"{self.image_base}{data.get(\\'poster_path\\')}" if data.get("poster_path") else None,
            "media_type": "tv"
        }
    
    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
''',

    "keyboards.py": '''"""
Inline keyboard layouts for the bot
All button configurations in one place
"""

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Dict
from config import get_button, FORCE_SUB_CHANNEL


def get_start_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Start command keyboard"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(get_button(lang, "help"), callback_data="help"),
            InlineKeyboardButton(get_button(lang, "profile"), callback_data="profile")
        ],
        [
            InlineKeyboardButton(get_button(lang, "request"), callback_data="start_request"),
            InlineKeyboardButton(get_button(lang, "leaderboard"), callback_data="leaderboard")
        ]
    ])


def get_help_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Help menu keyboard"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="start")]
    ])


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Language selection keyboard"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
            InlineKeyboardButton("🇱🇰 සිංහල", callback_data="lang_si")
        ]
    ])


def get_search_results_keyboard(
    results: List[Dict],
    page: int,
    total_pages: int,
    query: str,
    lang: str = "en"
) -> InlineKeyboardMarkup:
    """
    Search results keyboard with pagination
    
    Args:
        results: List of file dicts (max 10)
        page: Current page number (1-based)
        total_pages: Total number of pages
        query: Search query for pagination
        lang: Language code
    
    Returns:
        Inline keyboard with file buttons and pagination
    """
    from utils import format_file_size
    
    buttons = []
    
    # File buttons (10 max per page)
    for file in results:
        button_text = f"{format_file_size(file[\\'file_size\\'])} | {file[\\'clean_title\\']}"
        if file.get(\\'year\\'):
            button_text += f" | {file[\\'year\\']}"
        
        # Truncate if too long
        if len(button_text) > 64:
            button_text = button_text[:61] + "..."
        
        buttons.append([
            InlineKeyboardButton(button_text, callback_data=f"dl_{file[\\'file_id\\']}")
        ])
    
    # Pagination buttons
    pagination = []
    if page > 1:
        pagination.append(
            InlineKeyboardButton(get_button(lang, "prev"), callback_data=f"page_{query}_{page-1}")
        )
    
    pagination.append(
        InlineKeyboardButton(f"{page}/{total_pages}", callback_data="noop")
    )
    
    if page < total_pages:
        pagination.append(
            InlineKeyboardButton(get_button(lang, "next"), callback_data=f"page_{query}_{page+1}")
        )
    
    if pagination:
        buttons.append(pagination)
    
    return InlineKeyboardMarkup(buttons)


def get_force_sub_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Force subscribe keyboard"""
    if not FORCE_SUB_CHANNEL:
        return None
    
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(get_button(lang, "join_channel"), url=f"https://t.me/{FORCE_SUB_CHANNEL}")],
        [InlineKeyboardButton(get_button(lang, "check_subscription"), callback_data="check_sub")]
    ])


def get_request_results_keyboard(results: List[Dict]) -> InlineKeyboardMarkup:
    """TMDB search results keyboard"""
    buttons = []
    
    for result in results[:10]:  # Max 10
        media_type = result.get("media_type", "movie")
        title = result.get("title") or result.get("name", "Unknown")
        year = ""
        
        if media_type == "movie":
            year = result.get("release_date", "")[:4] if result.get("release_date") else ""
        else:
            year = result.get("first_air_date", "")[:4] if result.get("first_air_date") else ""
        
        button_text = f"{title} ({year})" if year else title
        
        # Truncate if needed
        if len(button_text) > 64:
            button_text = button_text[:61] + "..."
        
        buttons.append([
            InlineKeyboardButton(
                button_text,
                callback_data=f"req_{media_type}_{result[\\'id\\']}"
            )
        ])
    
    return InlineKeyboardMarkup(buttons)


def get_request_detail_keyboard(request_id: str, lang: str = "en") -> InlineKeyboardMarkup:
    """Request detail keyboard with request button"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(get_button(lang, "request_subtitle"), callback_data=f"submit_req_{request_id}")]
    ])


def get_admin_panel_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Admin panel keyboard"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📊 Statistics", callback_data="admin_stats"),
            InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")
        ],
        [
            InlineKeyboardButton("🔄 Index Channel", callback_data="admin_index"),
            InlineKeyboardButton("💾 Backup", callback_data="admin_backup")
        ],
        [
            InlineKeyboardButton("🔍 Scan Duplicates", callback_data="admin_scan")
        ]
    ])


def get_broadcast_confirm_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Broadcast confirmation keyboard"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(get_button(lang, "confirm"), callback_data="broadcast_confirm"),
            InlineKeyboardButton(get_button(lang, "cancel"), callback_data="broadcast_cancel")
        ]
    ])


def get_admin_request_keyboard(request_id: str, lang: str = "en") -> InlineKeyboardMarkup:
    """Admin request handling keyboard"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(get_button(lang, "done"), callback_data=f"req_done_{request_id}"),
            InlineKeyboardButton(get_button(lang, "not_available"), callback_data=f"req_no_{request_id}")
        ]
    ])


def get_duplicate_scan_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Duplicate scan action keyboard"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(get_button(lang, "delete_duplicates"), callback_data="delete_dupes")]
    ])
'''
}

# Create all files
def create_all_files():
    """Generate all remaining files"""
    for filename, content in FILES.items():
        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Created {filename}")
    
    print("\\nAll files created successfully!")

if __name__ == "__main__":
    create_all_files()
