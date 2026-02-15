"""
Admin command handlers
Handles all administrative commands
"""

import logging
import json
import asyncio
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from config import ADMIN_IDS, get_message
from keyboards import get_admin_panel_keyboard, get_broadcast_confirm_keyboard
from broadcast import BroadcastManager
from utils import format_timestamp

logger = logging.getLogger(__name__)

# Admin states
admin_states = {}


def register_admin_handlers(app: Client):
    """Register all admin command handlers"""
    
    # Admin filter
    admin_filter = filters.user(ADMIN_IDS) if ADMIN_IDS else filters.user([])
    
    @app.on_message(filters.command("admin") & filters.private & admin_filter)
    async def admin_panel(client: Client, message: Message):
        """Show admin panel"""
        try:
            await message.reply_text(
                get_message("en", "admin_panel"),
                reply_markup=get_admin_panel_keyboard()
            )
        except Exception as e:
            logger.error(f"Error in admin panel: {e}")
    
    @app.on_message(filters.command("stats") & filters.private & admin_filter)
    async def stats_command(client: Client, message: Message):
        """Show bot statistics"""
        try:
            db = client.db
            if not db:
                await message.reply_text("Database not available")
                return
            
            # Gather statistics
            total_users = await db.get_total_users()
            total_files = await db.get_total_files()
            total_downloads = await db.get_total_downloads()
            total_searches = await db.get_total_searches()
            pending_requests = await db.get_pending_requests_count()
            fulfilled_requests = await db.get_fulfilled_requests_count()
            
            # Top files
            top_files = await db.get_top_files(5)
            top_files_text = "\n".join([
                f"{idx}. {f.get(\'clean_title\', \'Unknown\')} - {f.get(\'downloads\', 0)} downloads"
                for idx, f in enumerate(top_files, 1)
            ]) if top_files else "No files yet"
            
            # Top users
            top_users = await db.get_top_users(5)
            top_users_text = "\n".join([
                f"{idx}. {u.get(\'first_name\', \'Unknown\')} - {u.get(\'downloads\', 0)} downloads"
                for idx, u in enumerate(top_users, 1)
            ]) if top_users else "No users yet"
            
            stats_text = get_message(
                "en",
                "stats",
                total_users=total_users,
                total_files=total_files,
                total_downloads=total_downloads,
                total_searches=total_searches,
                pending_requests=pending_requests,
                fulfilled_requests=fulfilled_requests,
                top_files=top_files_text,
                top_users=top_users_text
            )
            
            from config import STATS_IMAGE
            from image_handler import send_photo_safe, get_image_from_url
            
            photo = await get_image_from_url(client, STATS_IMAGE)
            await send_photo_safe(client, message.chat.id, photo, stats_text)
            
        except Exception as e:
            logger.error(f"Error in stats command: {e}")
    
    @app.on_message(filters.command("broadcast") & filters.private & admin_filter)
    async def broadcast_command(client: Client, message: Message):
        """Start broadcast process"""
        try:
            db = client.db
            if not db:
                return
            
            # Set admin state
            admin_states[message.from_user.id] = {"state": "awaiting_broadcast"}
            
            await message.reply_text(get_message("en", "broadcast_prompt"))
            
        except Exception as e:
            logger.error(f"Error in broadcast command: {e}")
    
    @app.on_message(filters.command("index") & filters.private & admin_filter)
    async def index_command(client: Client, message: Message):
        """Manually trigger channel indexing"""
        try:
            await message.reply_text(get_message("en", "indexing_started"))
            
            # This would trigger the indexer
            # Implementation depends on indexer design
            
        except Exception as e:
            logger.error(f"Error in index command: {e}")
    
    @app.on_message(filters.command("backup") & filters.private & admin_filter)
    async def backup_command(client: Client, message: Message):
        """Create database backup"""
        try:
            db = client.db
            if not db:
                return
            
            status_msg = await message.reply_text("Creating backup...")
            
            # Create backup
            backup_data = await db.create_backup()
            
            # Save to file
            filename = f"backup_{datetime.now().strftime(\'%Y%m%d_%H%M%S\')}.json"
            with open(filename, \'w\', encoding=\'utf-8\') as f:
                json.dump(backup_data, f, indent=2, default=str)
            
            # Send file
            await message.reply_document(filename, caption=get_message("en", "backup_created"))
            
            # Delete local file
            import os
            os.remove(filename)
            
            await status_msg.delete()
            
        except Exception as e:
            logger.error(f"Error in backup command: {e}")
    
    @app.on_message(filters.command("scan") & filters.private & admin_filter)
    async def scan_command(client: Client, message: Message):
        """Scan for duplicate files"""
        try:
            db = client.db
            if not db:
                return
            
            status_msg = await message.reply_text(get_message("en", "scan_started"))
            
            # Find duplicates
            duplicates = await db.find_duplicates()
            
            total_files = await db.get_total_files()
            duplicate_count = sum(len(dup_group) - 1 for dup_group in duplicates)
            
            scan_text = get_message(
                "en",
                "scan_complete",
                total=total_files,
                duplicates=duplicate_count
            )
            
            from keyboards import get_duplicate_scan_keyboard
            
            await status_msg.edit_text(
                scan_text,
                reply_markup=get_duplicate_scan_keyboard() if duplicate_count > 0 else None
            )
            
        except Exception as e:
            logger.error(f"Error in scan command: {e}")
    
    # Handle broadcast messages (catch-all for admin in broadcast state)
    @app.on_message(filters.private & admin_filter & ~filters.command(["stats", "broadcast", "index", "backup", "scan", "admin"]))
    async def handle_admin_message(client: Client, message: Message):
        """Handle admin messages (broadcast content)"""
        try:
            admin_state = admin_states.get(message.from_user.id, {})
            
            if admin_state.get("state") == "awaiting_broadcast":
                # Store broadcast message
                admin_states[message.from_user.id] = {
                    "state": "confirm_broadcast",
                    "message": message
                }
                
                db = client.db
                total_users = await db.get_total_users() if db else 0
                
                confirm_text = get_message(
                    "en",
                    "broadcast_confirm",
                    total_users=total_users
                )
                
                await message.reply_text(
                    confirm_text,
                    reply_markup=get_broadcast_confirm_keyboard()
                )
        
        except Exception as e:
            logger.error(f"Error handling admin message: {e}")
