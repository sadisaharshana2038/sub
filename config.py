"""
Configuration file for Telegram Subtitle Bot
Contains all settings, credentials, and multilingual messages
"""

import os
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================
# TELEGRAM CREDENTIALS
# ============================================
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BOT_USERNAME = os.getenv("BOT_USERNAME", "")

# ============================================
# MONGODB CONFIGURATION
# ============================================
MONGO_URI = os.getenv("MONGO_URI", "")
DATABASE_NAME = os.getenv("DATABASE_NAME", "subtitle_bot")

# ============================================
# CHANNEL IDS
# ============================================
SOURCE_CHANNEL_ID = int(os.getenv("SOURCE_CHANNEL_ID", "0")) or None
UPDATE_CHANNEL_ID = int(os.getenv("UPDATE_CHANNEL_ID", "0")) or None
ADMIN_CHANNEL_ID = int(os.getenv("ADMIN_CHANNEL_ID", "0")) or None
FORCE_SUB_CHANNEL = int(os.getenv("FORCE_SUB_CHANNEL", "0")) or None

# ============================================
# ADMIN IDS
# ============================================
ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "")
ADMIN_IDS: List[int] = [int(x.strip()) for x in ADMIN_IDS_STR.split(",") if x.strip().isdigit()]

# ============================================
# TMDB API (The Movie Database)
# ============================================
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# ============================================
# IMAGE URLS (Customizable)
# ============================================
WELCOME_IMAGE = os.getenv("WELCOME_IMAGE", "https://telegra.ph/file/example.jpg")
HELP_IMAGE = os.getenv("HELP_IMAGE", "https://telegra.ph/file/example.jpg")
STATS_IMAGE = os.getenv("STATS_IMAGE", "https://telegra.ph/file/example.jpg")
PROFILE_IMAGE = os.getenv("PROFILE_IMAGE", "https://telegra.ph/file/example.jpg")

# ============================================
# BOT SETTINGS
# ============================================
RESULTS_PER_PAGE = 10
MAX_PAGES = 5
MAX_RESULTS = RESULTS_PER_PAGE * MAX_PAGES  # 50 total
FUZZY_MATCH_THRESHOLD = 70
BROADCAST_BATCH_SIZE = 50
BROADCAST_DELAY = 1  # seconds between batches
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ============================================
# POINTS SYSTEM
# ============================================
POINTS_PER_DOWNLOAD = 1
POINTS_PER_REQUEST = 2

# ============================================
# RANK SYSTEM
# ============================================
RANKS = {
    "beginner": {"min": 0, "max": 9, "emoji": "🥉", "name_en": "Beginner", "name_si": "ආරම්භකයා"},
    "regular": {"min": 10, "max": 49, "emoji": "🥈", "name_en": "Regular User", "name_si": "සාමාන්‍ය පරිශීලක"},
    "active": {"min": 50, "max": 99, "emoji": "🥇", "name_en": "Active User", "name_si": "ක්‍රියාශීලී පරිශීලක"},
    "premium": {"min": 100, "max": 499, "emoji": "💎", "name_en": "Premium User", "name_si": "වාරික පරිශීලක"},
    "vip": {"min": 500, "max": 999, "emoji": "👑", "name_en": "VIP User", "name_si": "වී.අයි.පී පරිශීලක"},
    "legend": {"min": 1000, "max": float('inf'), "emoji": "🌟", "name_en": "Legend", "name_si": "පුරාවෘත්තය"}
}

# ============================================
# FILE EXTENSIONS (Subtitle files)
# ============================================
SUBTITLE_EXTENSIONS = [".srt", ".ass", ".ssa", ".sub", ".vtt", ".sbv"]

# ============================================
# MULTILINGUAL MESSAGES
# ============================================

MESSAGES = {
    "en": {
        # Welcome and Help
        "welcome": (
            "👋 <b>Welcome to Subtitle Bot!</b>\n\n"
            "🎬 I can help you find subtitle files for movies and TV shows.\n\n"
            "🔍 Just type the name of a movie or show to search!\n\n"
            "Use /help to see all available commands."
        ),
        "help": (
            "📚 <b>Help Menu</b>\n\n"
            "<b>🔍 Search Commands:</b>\n"
            "• Just type a movie/show name to search\n"
            "• Example: <code>Avatar</code> or <code>Breaking Bad</code>\n\n"
            "<b>👤 User Commands:</b>\n"
            "• /start - Start the bot\n"
            "• /help - Show this help menu\n"
            "• /language - Change language (English/Sinhala)\n"
            "• /profile - View your profile and stats\n"
            "• /request - Request a subtitle\n"
            "• /leaderboard - View top users\n\n"
            "<b>ℹ️ How to Use:</b>\n"
            "1. Type a movie or TV show name\n"
            "2. Browse through results (10 per page)\n"
            "3. Click on a subtitle to download\n"
            "4. Earn points for each download!\n\n"
            "<b>📊 Stats:</b>\n"
            "• 1 point per download\n"
            "• 2 points per request\n"
            "• Climb the leaderboard!\n\n"
            "Need help? Contact administrators!"
        ),
        
        # Search and Results
        "searching": "🔍 Searching for: <b>{query}</b>...",
        "no_results": "❌ No results found for: <b>{query}</b>\n\nTry:\n• Check spelling\n• Use different keywords\n• Request it using /request",
        "search_results": "🎬 <b>Search Results for:</b> {query}\n\n📄 Found {total} results (Showing page {page}/{total_pages})",
        "download_success": "✅ <b>Subtitle Downloaded!</b>\n\n📁 File: {filename}\n💎 You earned +{points} points!",
        "file_not_found": "❌ File not found. It may have been deleted from the source channel.",
        
        # Profile
        "profile": (
            "👤 <b>Your Profile</b>\n\n"
            "🆔 User ID: <code>{user_id}</code>\n"
            "👤 Name: {name}\n"
            "📥 Total Downloads: {downloads}\n"
            "💎 Points: {points}\n"
            "🏆 Rank: {rank_emoji} {rank_name}\n"
            "📅 Member Since: {join_date}\n"
            "⏰ Last Active: {last_active}"
        ),
        
        # Leaderboard
        "leaderboard": (
            "🏆 <b>Top Users Leaderboard</b>\n\n"
            "{leaderboard_text}\n\n"
            "💡 Keep downloading to climb higher!"
        ),
        "leaderboard_entry": "{rank}. {rank_emoji} {name} - {downloads} downloads ({points} pts)",
        
        # Request System
        "request_prompt": "🎬 Please type the name of the movie or TV show you want to request:",
        "request_searching_tmdb": "🔍 Searching TMDB for: <b>{query}</b>...",
        "request_no_results": "❌ No results found on TMDB for: <b>{query}</b>\n\nPlease try a different search term.",
        "request_select": "🎬 <b>Search Results:</b>\n\nSelect the correct title from the list below:",
        "request_details": (
            "🎬 <b>{title}</b> ({year})\n\n"
            "⭐ Rating: {rating}/10\n"
            "⏱️ Runtime: {runtime} minutes\n"
            "🎭 Genres: {genres}\n\n"
            "📝 <b>Overview:</b>\n{overview}\n\n"
            "Click the button below to request this subtitle!"
        ),
        "request_submitted": (
            "✅ <b>Request Submitted!</b>\n\n"
            "🎬 Title: {title}\n"
            "📅 Year: {year}\n\n"
            "We'll notify you once it's available!\n"
            "💎 You earned +{points} points!"
        ),
        "request_already_exists": "⚠️ You've already requested this title. Please wait for it to be fulfilled!",
        "request_fulfilled": "✅ <b>Good News!</b>\n\n🎬 Your request for <b>{title}</b> is now available!\n\nSearch for it to download.",
        "request_rejected": "❌ Sorry, <b>{title}</b> is not available at this time.",
        
        # Force Subscribe
        "force_sub": (
            "⚠️ <b>Join Our Channel First!</b>\n\n"
            "To use this bot, you must join our channel:\n"
            "👉 {channel_link}\n\n"
            "After joining, click the button below to verify."
        ),
        "not_subscribed": "❌ You haven't joined the channel yet!\n\nPlease join and try again.",
        "subscription_verified": "✅ Subscription verified! You can now use the bot.",
        
        # Language
        "language_select": "🌐 <b>Select Your Language:</b>\n\nChoose your preferred language below:",
        "language_changed": "✅ Language changed to: <b>English</b>",
        
        # Admin Messages
        "admin_panel": (
            "👨‍💼 <b>Admin Panel</b>\n\n"
            "Select an action from the buttons below:"
        ),
        "stats": (
            "📊 <b>Bot Statistics</b>\n\n"
            "👥 Total Users: {total_users}\n"
            "📁 Total Files: {total_files}\n"
            "📥 Total Downloads: {total_downloads}\n"
            "🔍 Total Searches: {total_searches}\n"
            "📝 Pending Requests: {pending_requests}\n"
            "✅ Fulfilled Requests: {fulfilled_requests}\n\n"
            "<b>🔥 Top 5 Most Downloaded:</b>\n{top_files}\n\n"
            "<b>👑 Top 5 Users:</b>\n{top_users}"
        ),
        "broadcast_prompt": "📢 Send the message you want to broadcast to all users.\n\nSupported: Text, Photo, Video, Document, Animation",
        "broadcast_confirm": "📢 <b>Confirm Broadcast</b>\n\n👥 Total Users: {total_users}\n\nAre you sure you want to send this message to all users?",
        "broadcast_cancelled": "❌ Broadcast cancelled.",
        "broadcast_started": "📢 <b>Broadcast Started!</b>\n\n👥 Total Users: {total_users}\n\nThis may take a while...",
        "broadcast_progress": "📢 <b>Broadcasting...</b>\n\n✅ Success: {success}\n❌ Failed: {failed}\n🚫 Blocked: {blocked}\n⏳ Remaining: {remaining}",
        "broadcast_complete": (
            "✅ <b>Broadcast Complete!</b>\n\n"
            "👥 Total Users: {total_users}\n"
            "✅ Successfully Sent: {success}\n"
            "❌ Failed: {failed}\n"
            "🚫 Blocked Bot: {blocked}\n"
            "⏱️ Time Taken: {time_taken}"
        ),
        "indexing_started": "🔄 Channel indexing started...",
        "indexing_complete": "✅ Indexing complete!\n\n📁 New files added: {new_files}\n⏱️ Time taken: {time_taken}",
        "backup_created": "✅ Database backup created successfully!",
        "scan_started": "🔍 Scanning for duplicate files...",
        "scan_complete": "✅ Scan complete!\n\n🔍 Total files: {total}\n📊 Duplicates found: {duplicates}\n\nUse the button below to delete duplicates.",
        "duplicates_deleted": "✅ {count} duplicate files deleted!",
        
        # Errors
        "error": "❌ An error occurred. Please try again later.",
        "error_db": "❌ Database error. Please contact administrators.",
        "admin_only": "⚠️ This command is only available to administrators.",
        "not_authorized": "⚠️ You are not authorized to use this command.",
        
        # Buttons
        "btn_help": "📚 Help",
        "btn_profile": "👤 Profile",
        "btn_request": "📝 Request Subtitle",
        "btn_leaderboard": "🏆 Leaderboard",
        "btn_next": "Next ▶️",
        "btn_prev": "◀️ Previous",
        "btn_download": "📥 Download",
        "btn_request_subtitle": "📝 Request Subtitle",
        "btn_join_channel": "📢 Join Channel",
        "btn_check_subscription": "✅ I Joined",
        "btn_english": "🇬🇧 English",
        "btn_sinhala": "🇱🇰 සිංහල",
        "btn_admin_stats": "📊 Statistics",
        "btn_admin_broadcast": "📢 Broadcast",
        "btn_admin_index": "🔄 Index Channel",
        "btn_admin_backup": "💾 Backup",
        "btn_admin_scan": "🔍 Scan Duplicates",
        "btn_confirm": "✅ Confirm",
        "btn_cancel": "❌ Cancel",
        "btn_delete_duplicates": "🗑️ Delete Duplicates",
        "btn_done": "✅ Done",
        "btn_not_available": "❌ Not Available",
    },
    
    "si": {  # Sinhala
        # Welcome and Help
        "welcome": (
            "👋 <b>උපසිරැසි බොට් වෙත සාදරයෙන් පිළිගනිමු!</b>\n\n"
            "🎬 මම ඔබට චිත්‍රපට සහ රූපවාහිනී වැඩසටහන් සඳහා උපසිරැසි ගොනු සොයා ගැනීමට උදව් කරමි.\n\n"
            "🔍 සෙවීමට චිත්‍රපටයක හෝ වැඩසටහනක නම ටයිප් කරන්න!\n\n"
            "සියලුම විධාන බැලීමට /help භාවිතා කරන්න."
        ),
        "help": (
            "📚 <b>උදව් මෙනුව</b>\n\n"
            "<b>🔍 සෙවුම් විධාන:</b>\n"
            "• චිත්‍රපට/වැඩසටහන් නමක් ටයිප් කරන්න\n"
            "• උදාහරණය: <code>Avatar</code> හෝ <code>Breaking Bad</code>\n\n"
            "<b>👤 පරිශීලක විධාන:</b>\n"
            "• /start - බොට් ආරම්භ කරන්න\n"
            "• /help - මෙම උදව් මෙනුව පෙන්වන්න\n"
            "• /language - භාෂාව වෙනස් කරන්න (ඉංග්‍රීසි/සිංහල)\n"
            "• /profile - ඔබේ පැතිකඩ බලන්න\n"
            "• /request - උපසිරැසියක් ඉල්ලන්න\n"
            "• /leaderboard - ඉහළම පරිශීලකයින් බලන්න\n\n"
            "<b>ℹ️ භාවිතා කරන්නේ කෙසේද:</b>\n"
            "1. චිත්‍රපටයක හෝ රූපවාහිනී වැඩසටහනක නම ටයිප් කරන්න\n"
            "2. ප්‍රතිඵල පිරික්සන්න (පිටුවකට 10)\n"
            "3. බාගත කිරීමට උපසිරැසියක් මත ක්ලික් කරන්න\n"
            "4. එක් එක් බාගත කිරීම සඳහා ලකුණු ලබා ගන්න!\n\n"
            "<b>📊 තොරතුරු:</b>\n"
            "• බාගත කිරීමකට ලකුණු 1ක්\n"
            "• ඉල්ලීමකට ලකුණු 2ක්\n"
            "• ලීඩර්බෝඩය තරණය කරන්න!\n\n"
            "උදව් අවශ්‍යද? පරිපාලකයින් සම්බන්ධ කරන්න!"
        ),
        
        # Search and Results
        "searching": "🔍 සෙවීම: <b>{query}</b>...",
        "no_results": "❌ ප්‍රතිඵල හමු නොවීය: <b>{query}</b>\n\nවෙනස් භාවිතා කරන්න:\n• අක්ෂර වින්‍යාසය පරීක්ෂා කරන්න\n• වෙනත් මූල පද භාවිතා කරන්න\n• /request භාවිතයෙන් ඉල්ලන්න",
        "search_results": "🎬 <b>සෙවුම් ප්‍රතිඵල:</b> {query}\n\n📄 ප්‍රතිඵල {total} හමු විය (පිටුව {page}/{total_pages} පෙන්වමින්)",
        "download_success": "✅ <b>උපසිරැසිය බාගත විය!</b>\n\n📁 ගොනුව: {filename}\n💎 ඔබ ලකුණු +{points} ලබා ගත්තා!",
        "file_not_found": "❌ ගොනුව හමු නොවීය. එය මූල නාලිකාවෙන් මකා දමා ඇති විය හැක.",
        
        # Profile
        "profile": (
            "👤 <b>ඔබේ පැතිකඩ</b>\n\n"
            "🆔 පරිශීලක හැඳුනුම්පත: <code>{user_id}</code>\n"
            "👤 නම: {name}\n"
            "📥 මුළු බාගත කිරීම්: {downloads}\n"
            "💎 ලකුණු: {points}\n"
            "🏆 ශ්‍රේණිය: {rank_emoji} {rank_name}\n"
            "📅 සාමාජිකත්වය: {join_date}\n"
            "⏰ අවසන් ක්‍රියාකාරිත්වය: {last_active}"
        ),
        
        # Leaderboard
        "leaderboard": (
            "🏆 <b>ඉහළ පරිශීලක ලීඩර්බෝඩය</b>\n\n"
            "{leaderboard_text}\n\n"
            "💡 ඉහළට යාමට බාගත කිරීම් දිගටම කරන්න!"
        ),
        "leaderboard_entry": "{rank}. {rank_emoji} {name} - බාගත {downloads} ({points} ලකුණු)",
        
        # Request System
        "request_prompt": "🎬 කරුණාකර ඔබට ඉල්ලීමට අවශ්‍ය චිත්‍රපටයේ හෝ රූපවාහිනී වැඩසටහනේ නම ටයිප් කරන්න:",
        "request_searching_tmdb": "🔍 TMDB හි සෙවීම: <b>{query}</b>...",
        "request_no_results": "❌ TMDB හි ප්‍රතිඵල හමු නොවීය: <b>{query}</b>\n\nකරුණාකර වෙනත් සෙවුම් පදයක් උත්සාහ කරන්න.",
        "request_select": "🎬 <b>සෙවුම් ප්‍රතිඵල:</b>\n\nපහත ලැයිස්තුවෙන් නිවැරදි මාතෘකාව තෝරන්න:",
        "request_details": (
            "🎬 <b>{title}</b> ({year})\n\n"
            "⭐ ශ්‍රේණිගත කිරීම: {rating}/10\n"
            "⏱️ දිග: මිනිත්තු {runtime}\n"
            "🎭 ප්‍රභේද: {genres}\n\n"
            "📝 <b>දළ විශ්ලේෂණය:</b>\n{overview}\n\n"
            "මෙම උපසිරැසිය ඉල්ලීමට පහත බොත්තම ක්ලික් කරන්න!"
        ),
        "request_submitted": (
            "✅ <b>ඉල්ලීම ඉදිරිපත් කළා!</b>\n\n"
            "🎬 මාතෘකාව: {title}\n"
            "📅 වර්ෂය: {year}\n\n"
            "එය ලබා ගත හැකි වූ පසු අපි ඔබට දන්වන්නෙමු!\n"
            "💎 ඔබ ලකුණු +{points} ලබා ගත්තා!"
        ),
        "request_already_exists": "⚠️ ඔබ මේ දැනටමත් ඉල්ලා ඇත. කරුණාකර එය සපුරාලන තෙක් රැඳී සිටින්න!",
        "request_fulfilled": "✅ <b>සුභ පුවත!</b>\n\n🎬 <b>{title}</b> සඳහා ඔබේ ඉල්ලීම දැන් ලබා ගත හැක!\n\nබාගත කිරීමට එය සොයන්න.",
        "request_rejected": "❌ සමාවන්න, <b>{title}</b> මේ මොහොතේ ලබා ගත නොහැක.",
        
        # Force Subscribe
        "force_sub": (
            "⚠️ <b>පළමුව අපේ නාලිකාවට එක්වන්න!</b>\n\n"
            "මෙම බොට් භාවිතා කිරීමට, ඔබ අපේ නාලිකාවට එක් විය යුතුයි:\n"
            "👉 {channel_link}\n\n"
            "එක් වීමෙන් පසු, සත්‍යාපනය කිරීමට පහත බොත්තම ක්ලික් කරන්න."
        ),
        "not_subscribed": "❌ ඔබ තවමත් නාලිකාවට එක්ව නැත!\n\nකරුණාකර එක්වී නැවත උත්සාහ කරන්න.",
        "subscription_verified": "✅ දායකත්වය සත්‍යාපනය විය! ඔබට දැන් බොට් භාවිතා කළ හැකිය.",
        
        # Language
        "language_select": "🌐 <b>ඔබේ භාෂාව තෝරන්න:</b>\n\nපහතින් ඔබේ කැමති භාෂාව තෝරන්න:",
        "language_changed": "✅ භාෂාව වෙනස් විය: <b>සිංහල</b>",
        
        # Admin Messages (keeping English for clarity in admin functions)
        "admin_panel": (
            "👨‍💼 <b>පරිපාලක පැනලය</b>\n\n"
            "පහත බොත්තම් වලින් ක්‍රියාවක් තෝරන්න:"
        ),
        "stats": (
            "📊 <b>බොට් සංඛ්‍යාලේඛන</b>\n\n"
            "👥 මුළු පරිශීලකයින්: {total_users}\n"
            "📁 මුළු ගොනු: {total_files}\n"
            "📥 මුළු බාගත කිරීම්: {total_downloads}\n"
            "🔍 මුළු සෙවීම්: {total_searches}\n"
            "📝 පොරොත්තු ඉල්ලීම්: {pending_requests}\n"
            "✅ සම්පූර්ණ ඉල්ලීම්: {fulfilled_requests}\n\n"
            "<b>🔥 වැඩිම බාගත කළ 5:</b>\n{top_files}\n\n"
            "<b>👑 ඉහළ පරිශීලකයින් 5:</b>\n{top_users}"
        ),
        "broadcast_prompt": "📢 සියලු පරිශීලකයින්ට විකාශනය කිරීමට අවශ්‍ය පණිවිඩය යවන්න.\n\nසහාය දක්වයි: පෙළ, ඡායාරූප, වීඩියෝ, ලේඛන, සජීවීකරණ",
        "broadcast_confirm": "📢 <b>විකාශනය සනාථ කරන්න</b>\n\n👥 මුළු පරිශීලකයින්: {total_users}\n\nඔබට මෙම පණිවිඩය සියලු පරිශීලකයින්ට යැවීමට අවශ්‍ය බව විශ්වාසද?",
        "broadcast_cancelled": "❌ විකාශනය අවලංගු විය.",
        "broadcast_started": "📢 <b>විකාශනය ආරම්භ විය!</b>\n\n👥 මුළු පරිශීලකයින්: {total_users}\n\nමෙයට යම් කාලයක් ගත විය හැක...",
        "broadcast_progress": "📢 <b>විකාශනය වෙමින්...</b>\n\n✅ සාර්ථක: {success}\n❌ අසාර්ථක: {failed}\n🚫 අවහිර කළා: {blocked}\n⏳ ඉතිරිය: {remaining}",
        "broadcast_complete": (
            "✅ <b>විකාශනය සම්පූර්ණයි!</b>\n\n"
            "👥 මුළු පරිශීලකයින්: {total_users}\n"
            "✅ සාර්ථකව යැවීය: {success}\n"
            "❌ අසාර්ථකයි: {failed}\n"
            "🚫 බොට් අවහිර කළා: {blocked}\n"
            "⏱️ ගත වූ කාලය: {time_taken}"
        ),
        
        # Buttons
        "btn_help": "📚 උදව්",
        "btn_profile": "👤 පැතිකඩ",
        "btn_request": "📝 උපසිරැසි ඉල්ලන්න",
        "btn_leaderboard": "🏆 ලීඩර්බෝඩය",
        "btn_next": "ඊළඟ ▶️",
        "btn_prev": "◀️ පෙර",
        "btn_download": "📥 බාගත කරන්න",
        "btn_request_subtitle": "📝 උපසිරැසි ඉල්ලන්න",
        "btn_join_channel": "📢 නාලිකාවට එක්වන්න",
        "btn_check_subscription": "✅ මම එක් වුණා",
        "btn_english": "🇬🇧 English",
        "btn_sinhala": "🇱🇰 සිංහල",
        "btn_confirm": "✅ සනාථ කරන්න",
        "btn_cancel": "❌ අවලංගු කරන්න",
        "btn_done": "✅ අවසන්",
        "btn_not_available": "❌ නොමැත",
    }
}


def get_message(lang: str, key: str, **kwargs) -> str:
    """
    Get message in specified language with formatting
    
    Args:
        lang: Language code ('en' or 'si')
        key: Message key
        **kwargs: Format parameters
    
    Returns:
        Formatted message string
    """
    try:
        # Default to English if language not found
        if lang not in MESSAGES:
            lang = "en"
        
        # Get message
        message = MESSAGES[lang].get(key, MESSAGES["en"].get(key, ""))
        
        # Format with parameters
        if kwargs:
            message = message.format(**kwargs)
        
        return message
    except Exception as e:
        # Fallback to English
        try:
            return MESSAGES["en"][key].format(**kwargs)
        except:
            return f"Error loading message: {key}"


# Helper function to get button text
def get_button(lang: str, key: str) -> str:
    """Get button text in specified language"""
    return get_message(lang, f"btn_{key}")
