"""
Notifier Agent - Sends notifications when content is ready
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any

class NotifierAgent:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def send_completion_notification(self, pipeline_data: Dict[str, Any]) -> None:
        """Send notification that content generation is complete"""
        self.logger.info("📢 Sending completion notifications...")
        
        # CLI notification (always enabled)
        self._send_cli_notification(pipeline_data)
        
        # Telegram notification (if configured)
        if os.getenv('TELEGRAM_BOT_TOKEN') and os.getenv('TELEGRAM_CHAT_ID'):
            self._send_telegram_notification(pipeline_data)
        
        # Email notification (if configured)
        # TODO: Implement email notifications
        
    def _send_cli_notification(self, pipeline_data: Dict[str, Any]) -> None:
        """Send CLI notification with summary"""
        
        print("\n" + "="*60)
        print("🎉 XTHREADS AGENT - DAILY RUN COMPLETE")
        print("="*60)
        
        # Summary stats
        generated_posts = pipeline_data.get('generated_posts', {})
        total_posts = sum(len(posts) for posts in generated_posts.values())
        successful_posts = sum(
            len([p for p in posts if p.get('status') == 'success']) 
            for posts in generated_posts.values()
        )
        
        print(f"📊 SUMMARY:")
        print(f"   • Total posts planned: {total_posts}")
        print(f"   • Successfully generated: {successful_posts}")
        print(f"   • Success rate: {(successful_posts/total_posts*100):.1f}%" if total_posts > 0 else "   • Success rate: 0%")
        
        # Platform breakdown
        print(f"\n📱 PLATFORM BREAKDOWN:")
        for platform, posts in generated_posts.items():
            ready_count = len([p for p in posts if p.get('status') == 'success'])
            total_count = len(posts)
            print(f"   • {platform.title()}: {ready_count}/{total_count} posts ready")
        
        # Export files
        export_files = pipeline_data.get('export_files', [])
        if export_files:
            print(f"\n📤 EXPORTED FILES:")
            for file_path in export_files:
                print(f"   • {file_path}")
        
        # Next steps
        print(f"\n🚀 NEXT STEPS:")
        print(f"   1. Review generated content in exported files")
        print(f"   2. Copy and paste posts to respective platforms")
        print(f"   3. Schedule posts for optimal UK times")
        print(f"   4. Monitor engagement and adjust strategy")
        
        print("\n" + "="*60)
        print(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UK")
        print("="*60 + "\n")
    
    def _send_telegram_notification(self, pipeline_data: Dict[str, Any]) -> None:
        """Send Telegram notification"""
        try:
            import requests
            
            bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
            chat_id = os.getenv('TELEGRAM_CHAT_ID')
            
            # Prepare message
            generated_posts = pipeline_data.get('generated_posts', {})
            total_posts = sum(len(posts) for posts in generated_posts.values())
            successful_posts = sum(
                len([p for p in posts if p.get('status') == 'success']) 
                for posts in generated_posts.values()
            )
            
            message = f"""🤖 *xthreads\\_agent Daily Report*
            
📊 *Summary:*
• Total posts: {total_posts}
• Generated successfully: {successful_posts}
• Success rate: {(successful_posts/total_posts*100):.1f}%

📱 *Platform Breakdown:*
"""
            
            for platform, posts in generated_posts.items():
                ready_count = len([p for p in posts if p.get('status') == 'success'])
                total_count = len(posts)
                message += f"• {platform.title()}: {ready_count}/{total_count}\n"
            
            message += f"\n✅ Content is ready for posting!"
            message += f"\n📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} UK"
            
            # Send message
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                self.logger.info("✅ Telegram notification sent")
            else:
                self.logger.error(f"Telegram notification failed: {response.text}")
                
        except Exception as e:
            self.logger.error(f"Telegram notification error: {e}")
    
    def send_error_notification(self, error_message: str) -> None:
        """Send error notification"""
        self.logger.error("❌ XTHREADS AGENT ERROR")
        self.logger.error(f"Error: {error_message}")
        
        # CLI error notification
        print("\n" + "="*60)
        print("❌ XTHREADS AGENT - ERROR OCCURRED")
        print("="*60)
        print(f"Error: {error_message}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UK")
        print("Check logs for more details.")
        print("="*60 + "\n")
        
        # Telegram error notification (if configured)
        if os.getenv('TELEGRAM_BOT_TOKEN') and os.getenv('TELEGRAM_CHAT_ID'):
            try:
                import requests
                
                bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
                chat_id = os.getenv('TELEGRAM_CHAT_ID')
                
                message = f"""❌ *xthreads\\_agent Error*
                
Error: `{error_message}`
Time: {datetime.now().strftime('%Y-%m-%d %H:%M')} UK

Please check the logs for more details."""
                
                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                data = {
                    'chat_id': chat_id,
                    'text': message,
                    'parse_mode': 'Markdown'
                }
                
                requests.post(url, data=data)
                
            except Exception as e:
                self.logger.error(f"Error notification failed: {e}")