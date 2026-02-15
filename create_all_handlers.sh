#!/bin/bash

# Create force_subscribe.py
cat > force_subscribe.py << 'EOF'
"""
Force subscribe module
Checks if user has joined required channel before using bot
"""

import logging
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant, ChatAdminRequired
from config import FORCE_SUB_CHANNEL
from keyboards import get_force_sub_keyboard

logger = logging.getLogger(__name__)


async def check_force_sub(client: Client, user_id: int) -> bool:
    """
    Check if user has joined the required channel
    
    Args:
        client: Pyrogram client
        user_id: User ID to check
    
    Returns:
        True if subscribed or no force sub enabled, False otherwise
    """
    try:
        # If no force sub channel configured, allow access
        if not FORCE_SUB_CHANNEL:
            return True
        
        # Check user membership
        member = await client.get_chat_member(FORCE_SUB_CHANNEL, user_id)
        
        # Allow if user is member, admin, or creator
        if member.status in ["member", "administrator", "creator"]:
            return True
        
        return False
        
    except UserNotParticipant:
        return False
    except ChatAdminRequired:
        logger.error("Bot is not admin in force sub channel!")
        return True  # Allow access if bot can't check
    except Exception as e:
        logger.error(f"Error checking force sub: {e}")
        return True  # Allow access on error


async def handle_force_sub(message: Message, lang: str = "en") -> bool:
    """
    Handle force subscribe check and send message if needed
    
    Args:
        message: Pyrogram message
        lang: Language code
    
    Returns:
        True if user is subscribed, False otherwise
    """
    try:
        from config import get_message
        
        is_subscribed = await check_force_sub(message._client, message.from_user.id)
        
        if not is_subscribed:
            # Send force subscribe message
            await message.reply_text(
                get_message(lang, "force_sub", channel_link=f"https://t.me/{FORCE_SUB_CHANNEL}"),
                reply_markup=get_force_sub_keyboard(lang)
            )
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error handling force sub: {e}")
        return True  # Allow on error
EOF

# Create broadcast.py
cat > broadcast.py << 'EOF'
"""
Broadcast module for sending messages to all users
Advanced broadcasting with progress tracking and error handling
"""

import logging
import asyncio
from datetime import datetime
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from database import Database
from config import BROADCAST_BATCH_SIZE, BROADCAST_DELAY
from utils import batch_list, create_progress_bar, format_duration

logger = logging.getLogger(__name__)


class BroadcastManager:
    """Manage broadcast operations"""
    
    def __init__(self, client: Client, db: Database):
        """Initialize broadcast manager"""
        self.client = client
        self.db = db
    
    async def broadcast_message(
        self,
        message: Message,
        admin_id: int,
        progress_msg: Message = None
    ) -> dict:
        """
        Broadcast a message to all users
        
        Args:
            message: Message to broadcast
            admin_id: Admin user ID
            progress_msg: Message to update with progress
        
        Returns:
            Statistics dict
        """
        start_time = datetime.now()
        
        # Get all user IDs
        user_ids = await self.db.get_all_user_ids()
        total_users = len(user_ids)
        
        # Create broadcast record
        broadcast_id = await self.db.create_broadcast(admin_id, total_users)
        
        # Statistics
        stats = {
            "total": total_users,
            "success": 0,
            "failed": 0,
            "blocked": 0
        }
        
        # Process in batches
        for batch_num, batch in enumerate(batch_list(user_ids, BROADCAST_BATCH_SIZE), 1):
            # Send to batch
            for user_id in batch:
                try:
                    # Copy message based on type
                    if message.text:
                        await self.client.send_message(user_id, message.text)
                    elif message.photo:
                        await self.client.send_photo(
                            user_id,
                            message.photo.file_id,
                            caption=message.caption
                        )
                    elif message.video:
                        await self.client.send_video(
                            user_id,
                            message.video.file_id,
                            caption=message.caption
                        )
                    elif message.document:
                        await self.client.send_document(
                            user_id,
                            message.document.file_id,
                            caption=message.caption
                        )
                    elif message.animation:
                        await self.client.send_animation(
                            user_id,
                            message.animation.file_id,
                            caption=message.caption
                        )
                    
                    stats["success"] += 1
                    
                except (UserIsBlocked, InputUserDeactivated):
                    stats["blocked"] += 1
                except FloodWait as e:
                    logger.warning(f"FloodWait: {e.value} seconds")
                    await asyncio.sleep(e.value)
                    # Retry once
                    try:
                        await self.client.send_message(user_id, message.text or "Message")
                        stats["success"] += 1
                    except:
                        stats["failed"] += 1
                except Exception as e:
                    logger.error(f"Broadcast error for user {user_id}: {e}")
                    stats["failed"] += 1
            
            # Update database stats
            await self.db.update_broadcast_stats(
                broadcast_id,
                success=len([u for u in batch if u]),  # Batch success count
            )
            
            # Update progress message
            if progress_msg and batch_num % 5 == 0:  # Update every 5 batches
                try:
                    from config import get_message
                    
                    progress_text = get_message(
                        "en",
                        "broadcast_progress",
                        success=stats["success"],
                        failed=stats["failed"],
                        blocked=stats["blocked"],
                        remaining=total_users - stats["success"] - stats["failed"] - stats["blocked"]
                    )
                    
                    # Add progress bar
                    completed = stats["success"] + stats["failed"] + stats["blocked"]
                    progress_bar = create_progress_bar(completed, total_users)
                    progress_text += f"\\n\\n{progress_bar}"
                    
                    await progress_msg.edit_text(progress_text)
                except:
                    pass
            
            # Delay between batches
            await asyncio.sleep(BROADCAST_DELAY)
        
        # Mark broadcast complete
        await self.db.complete_broadcast(broadcast_id)
        
        # Calculate time taken
        end_time = datetime.now()
        time_taken = format_duration(int((end_time - start_time).total_seconds()))
        stats["time_taken"] = time_taken
        
        return stats
EOF

# Create image_handler.py
cat > image_handler.py << 'EOF'
"""
Image handler for Telegram and Telegraph image URLs
Handles both t.me links and telegra.ph links gracefully
"""

import logging
from pyrogram import Client
from pyrogram.types import InputMediaPhoto
from utils import extract_telegram_file_id, parse_telegram_image_url

logger = logging.getLogger(__name__)


async def get_image_from_url(client: Client, url: str) -> str:
    """
    Get image file_id from URL (Telegram or Telegraph)
    
    Args:
        client: Pyrogram client
        url: Image URL
    
    Returns:
        File ID or URL for sending
    """
    try:
        if not url:
            return None
        
        # Parse URL
        parsed_url = parse_telegram_image_url(url)
        if not parsed_url:
            return None
        
        # Check if it's a Telegram link
        telegram_data = extract_telegram_file_id(parsed_url)
        if telegram_data:
            channel, message_id = telegram_data
            
            try:
                # Get message from channel
                message = await client.get_messages(f"@{channel}", message_id)
                
                if message and message.photo:
                    return message.photo.file_id
            except Exception as e:
                logger.warning(f"Could not fetch Telegram image: {e}")
        
        # Return URL for Telegraph or other links
        return parsed_url
        
    except Exception as e:
        logger.error(f"Error getting image from URL: {e}")
        return None


async def send_photo_safe(client: Client, chat_id: int, photo: str, caption: str = None, **kwargs):
    """
    Safely send photo with fallback to text
    
    Args:
        client: Pyrogram client
        chat_id: Chat ID
        photo: Photo file_id or URL
        caption: Caption text
        **kwargs: Additional arguments for send_photo
    """
    try:
        if photo:
            # Try to send photo
            await client.send_photo(chat_id, photo, caption=caption, **kwargs)
        else:
            # Fallback to text only
            if caption:
                await client.send_message(chat_id, caption, **kwargs)
    except Exception as e:
        logger.warning(f"Error sending photo, falling back to text: {e}")
        # Fallback to text only
        if caption:
            try:
                await client.send_message(chat_id, caption, **kwargs)
            except:
                pass
EOF

echo "✓ Created force_subscribe.py"
echo "✓ Created broadcast.py"
echo "✓ Created image_handler.py"
echo "All support modules created successfully!"
