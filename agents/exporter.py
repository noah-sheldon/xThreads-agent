"""
Exporter Agent - Exports generated content to various formats
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

import pandas as pd

class ExporterAgent:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize export directory
        self.export_dir = Path("data/exports")
        self.export_dir.mkdir(parents=True, exist_ok=True)
        
    def export_content_calendar(self, generated_posts: Dict[str, List[Dict]]) -> List[str]:
        """Export content calendar in multiple formats"""
        self.logger.info("📤 Exporting content calendar...")
        
        # Prepare data for export
        calendar_data = self._prepare_calendar_data(generated_posts)
        
        today = datetime.now().strftime("%Y-%m-%d")
        exported_files = []
        
        # Export as Excel
        excel_file = self._export_excel(calendar_data, today)
        if excel_file:
            exported_files.append(excel_file)
            
        # Export as CSV
        csv_file = self._export_csv(calendar_data, today)
        if csv_file:
            exported_files.append(csv_file)
            
        # Export as Markdown
        md_file = self._export_markdown(calendar_data, today)
        if md_file:
            exported_files.append(md_file)
            
        # Export as JSON (backup)
        json_file = self._export_json(generated_posts, today)
        if json_file:
            exported_files.append(json_file)
        
        self.logger.info(f"✅ Exported {len(exported_files)} files")
        return exported_files
    
    def _prepare_calendar_data(self, generated_posts: Dict[str, List[Dict]]) -> List[Dict]:
        """Prepare data in a flat structure for export"""
        calendar_data = []
        today = datetime.now().strftime("%Y-%m-%d")
        
        for platform, posts in generated_posts.items():
            for post in posts:
                row = {
                    'Date': today,
                    'Platform': platform.title(),
                    'Time (UK)': post.get('posting_time_uk', '12:00'),
                    'Content Type': post.get('content_type', 'general').title(),
                    'Topic': post.get('topic', 'N/A'),
                    'Content': post.get('generated_content', 'Failed to generate'),
                    'Status': 'Ready' if post.get('status') == 'success' else 'Failed',
                    'Target Keywords': ', '.join(post.get('target_keywords', [])),
                    'Call to Action': post.get('call_to_action', ''),
                    'Max Characters': post.get('max_chars', 'N/A'),
                    'Character Count': len(post.get('generated_content', '')),
                    'Generated At': post.get('generated_at', datetime.now()).strftime('%H:%M:%S'),
                    'Attempts': post.get('attempt', 1)
                }
                calendar_data.append(row)
        
        # Sort by platform and time
        calendar_data.sort(key=lambda x: (x['Platform'], x['Time (UK)']))
        return calendar_data
    
    def _export_excel(self, calendar_data: List[Dict], date: str) -> str:
        """Export to Excel format"""
        try:
            df = pd.DataFrame(calendar_data)
            
            file_path = self.export_dir / f"content-calendar-{date}.xlsx"
            
            # Create Excel writer with formatting
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Content Calendar', index=False)
                
                # Get workbook and worksheet
                workbook = writer.book
                worksheet = writer.sheets['Content Calendar']
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    
                    adjusted_width = min(max_length + 2, 50)  # Cap at 50 chars
                    worksheet.column_dimensions[column_letter].width = adjusted_width
                
                # Add summary sheet
                summary_data = self._create_summary_data(calendar_data)
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            self.logger.info(f"✅ Excel exported: {file_path}")
            return str(file_path)
            
        except Exception as e:
            self.logger.error(f"Excel export failed: {e}")
            return None
    
    def _export_csv(self, calendar_data: List[Dict], date: str) -> str:
        """Export to CSV format"""
        try:
            df = pd.DataFrame(calendar_data)
            file_path = self.export_dir / f"content-calendar-{date}.csv"
            df.to_csv(file_path, index=False)
            
            self.logger.info(f"✅ CSV exported: {file_path}")
            return str(file_path)
            
        except Exception as e:
            self.logger.error(f"CSV export failed: {e}")
            return None
    
    def _export_markdown(self, calendar_data: List[Dict], date: str) -> str:
        """Export to Markdown format"""
        try:
            file_path = self.export_dir / f"content-calendar-{date}.md"
            
            with open(file_path, 'w') as f:
                f.write(f"# Content Calendar - {date}\n\n")
                f.write("Generated by xthreads_agent 🤖\n\n")
                
                # Group by platform
                platforms = {}
                for row in calendar_data:
                    platform = row['Platform']
                    if platform not in platforms:
                        platforms[platform] = []
                    platforms[platform].append(row)
                
                for platform, posts in platforms.items():
                    f.write(f"## {platform}\n\n")
                    
                    for post in posts:
                        f.write(f"### {post['Time (UK)']} - {post['Content Type']}\n\n")
                        f.write(f"**Topic:** {post['Topic']}\n\n")
                        f.write(f"**Content:**\n```\n{post['Content']}\n```\n\n")
                        f.write(f"**Keywords:** {post['Target Keywords']}\n\n")
                        f.write(f"**Status:** {post['Status']} | **Characters:** {post['Character Count']}\n\n")
                        f.write("---\n\n")
            
            self.logger.info(f"✅ Markdown exported: {file_path}")
            return str(file_path)
            
        except Exception as e:
            self.logger.error(f"Markdown export failed: {e}")
            return None
    
    def _export_json(self, generated_posts: Dict[str, List[Dict]], date: str) -> str:
        """Export raw JSON backup"""
        try:
            file_path = self.export_dir / f"content-backup-{date}.json"
            
            with open(file_path, 'w') as f:
                json.dump(generated_posts, f, indent=2, default=str)
            
            self.logger.info(f"✅ JSON backup exported: {file_path}")
            return str(file_path)
            
        except Exception as e:
            self.logger.error(f"JSON export failed: {e}")
            return None
    
    def _create_summary_data(self, calendar_data: List[Dict]) -> List[Dict]:
        """Create summary statistics"""
        summary = []
        
        # Platform breakdown
        platforms = {}
        total_posts = len(calendar_data)
        successful_posts = len([p for p in calendar_data if p['Status'] == 'Ready'])
        
        for row in calendar_data:
            platform = row['Platform']
            if platform not in platforms:
                platforms[platform] = {'total': 0, 'ready': 0}
            platforms[platform]['total'] += 1
            if row['Status'] == 'Ready':
                platforms[platform]['ready'] += 1
        
        # Add summary rows
        summary.append({
            'Metric': 'Total Posts Planned',
            'Value': total_posts
        })
        
        summary.append({
            'Metric': 'Successfully Generated',
            'Value': successful_posts
        })
        
        summary.append({
            'Metric': 'Success Rate',
            'Value': f"{(successful_posts/total_posts*100):.1f}%" if total_posts > 0 else "0%"
        })
        
        # Platform breakdown
        for platform, stats in platforms.items():
            summary.append({
                'Metric': f'{platform} Posts',
                'Value': f"{stats['ready']}/{stats['total']}"
            })
        
        return summary