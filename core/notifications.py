"""
Enterprise Email Notification System for gcPanel Construction Platform

Automated email notifications for project updates, alerts, and reports
with professional templates and delivery tracking.
"""

import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from typing import Dict, List, Optional
import streamlit as st
from core.database import get_database

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationManager:
    """Enterprise email notification system with professional templates."""
    
    def __init__(self):
        """Initialize notification system."""
        self.db = get_database()
        
        # Email configuration
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        self.smtp_username = os.environ.get('SMTP_USERNAME')
        self.smtp_password = os.environ.get('SMTP_PASSWORD')
        self.from_email = os.environ.get('FROM_EMAIL', self.smtp_username)
        self.from_name = os.environ.get('FROM_NAME', 'gcPanel Construction')
        
        # Notification settings
        self.max_retries = 3
        self.batch_size = 10
        
        # Email templates
        self.templates = self._load_email_templates()
    
    def _load_email_templates(self) -> Dict:
        """Load professional email templates for construction notifications."""
        return {
            'daily_report_submitted': {
                'subject': 'Daily Report Submitted - {project_name}',
                'template': '''
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: #2E86AB; color: white; padding: 20px; text-align: center;">
                        <h2>📋 Daily Report Submitted</h2>
                    </div>
                    <div style="padding: 20px; background: #f8f9fa;">
                        <p>Hello {recipient_name},</p>
                        <p>A new daily report has been submitted for your project:</p>
                        
                        <div style="background: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                            <h3 style="color: #2E86AB; margin-top: 0;">Project Details</h3>
                            <p><strong>Project:</strong> {project_name}</p>
                            <p><strong>Report Date:</strong> {report_date}</p>
                            <p><strong>Submitted By:</strong> {submitted_by}</p>
                            <p><strong>Weather:</strong> {weather}</p>
                            <p><strong>Crew Size:</strong> {crew_size}</p>
                        </div>
                        
                        <div style="background: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                            <h4>Work Performed:</h4>
                            <p>{work_performed}</p>
                        </div>
                        
                        <div style="text-align: center; margin: 20px 0;">
                            <a href="{platform_url}" style="background: #2E86AB; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px;">
                                View Full Report
                            </a>
                        </div>
                        
                        <hr style="margin: 20px 0;">
                        <p style="color: #666; font-size: 12px;">
                            This is an automated notification from gcPanel Construction Management Platform.
                        </p>
                    </div>
                </div>
                '''
            },
            
            'inspection_completed': {
                'subject': 'Quality Inspection Completed - {inspection_type}',
                'template': '''
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: #28A745; color: white; padding: 20px; text-align: center;">
                        <h2>🔍 Quality Inspection Completed</h2>
                    </div>
                    <div style="padding: 20px; background: #f8f9fa;">
                        <p>Hello {recipient_name},</p>
                        <p>A quality inspection has been completed:</p>
                        
                        <div style="background: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                            <h3 style="color: #28A745; margin-top: 0;">Inspection Details</h3>
                            <p><strong>Inspection Type:</strong> {inspection_type}</p>
                            <p><strong>Project:</strong> {project_name}</p>
                            <p><strong>Location:</strong> {location}</p>
                            <p><strong>Inspector:</strong> {inspector_name}</p>
                            <p><strong>Status:</strong> <span style="color: {status_color}; font-weight: bold;">{final_status}</span></p>
                            <p><strong>Score:</strong> {inspection_score}%</p>
                        </div>
                        
                        {deficiencies_section}
                        
                        <div style="text-align: center; margin: 20px 0;">
                            <a href="{platform_url}" style="background: #28A745; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px;">
                                View Inspection Report
                            </a>
                        </div>
                        
                        <hr style="margin: 20px 0;">
                        <p style="color: #666; font-size: 12px;">
                            This is an automated notification from gcPanel Construction Management Platform.
                        </p>
                    </div>
                </div>
                '''
            },
            
            'payment_application_submitted': {
                'subject': 'Payment Application #{application_number} Submitted',
                'template': '''
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: #FFC107; color: #000; padding: 20px; text-align: center;">
                        <h2>💰 Payment Application Submitted</h2>
                    </div>
                    <div style="padding: 20px; background: #f8f9fa;">
                        <p>Hello {recipient_name},</p>
                        <p>A new payment application has been submitted for approval:</p>
                        
                        <div style="background: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                            <h3 style="color: #FFC107; margin-top: 0;">Payment Application Details</h3>
                            <p><strong>Application #:</strong> {application_number}</p>
                            <p><strong>Project:</strong> {project_name}</p>
                            <p><strong>Period:</strong> {period_from} to {period_to}</p>
                            <p><strong>Contract Sum:</strong> ${contract_sum:,.2f}</p>
                            <p><strong>Payment Due:</strong> <span style="color: #28A745; font-weight: bold;">${payment_due:,.2f}</span></p>
                        </div>
                        
                        <div style="text-align: center; margin: 20px 0;">
                            <a href="{platform_url}" style="background: #FFC107; color: #000; padding: 12px 25px; text-decoration: none; border-radius: 5px;">
                                Review Application
                            </a>
                        </div>
                        
                        <hr style="margin: 20px 0;">
                        <p style="color: #666; font-size: 12px;">
                            This is an automated notification from gcPanel Construction Management Platform.
                        </p>
                    </div>
                </div>
                '''
            },
            
            'safety_incident_alert': {
                'subject': '🚨 URGENT: Safety Incident Reported - {project_name}',
                'template': '''
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: #DC3545; color: white; padding: 20px; text-align: center;">
                        <h2>🚨 SAFETY INCIDENT ALERT</h2>
                    </div>
                    <div style="padding: 20px; background: #f8f9fa;">
                        <p><strong>URGENT NOTIFICATION</strong></p>
                        <p>Hello {recipient_name},</p>
                        <p>A safety incident has been reported that requires immediate attention:</p>
                        
                        <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 15px 0;">
                            <h3 style="color: #DC3545; margin-top: 0;">Incident Details</h3>
                            <p><strong>Project:</strong> {project_name}</p>
                            <p><strong>Date/Time:</strong> {incident_date}</p>
                            <p><strong>Location:</strong> {location}</p>
                            <p><strong>Severity:</strong> <span style="color: #DC3545; font-weight: bold;">{severity}</span></p>
                            <p><strong>Reported By:</strong> {reported_by}</p>
                        </div>
                        
                        <div style="background: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                            <h4>Description:</h4>
                            <p>{incident_description}</p>
                        </div>
                        
                        <div style="text-align: center; margin: 20px 0;">
                            <a href="{platform_url}" style="background: #DC3545; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px;">
                                View Incident Report
                            </a>
                        </div>
                        
                        <p style="color: #DC3545; font-weight: bold;">
                            Please take immediate action to address this incident.
                        </p>
                        
                        <hr style="margin: 20px 0;">
                        <p style="color: #666; font-size: 12px;">
                            This is an automated urgent notification from gcPanel Construction Management Platform.
                        </p>
                    </div>
                </div>
                '''
            }
        }
    
    def send_daily_report_notification(self, report_data: Dict, recipients: List[str]) -> Dict:
        """Send notification for daily report submission."""
        try:
            template_data = {
                'project_name': report_data.get('project_name', 'Unknown Project'),
                'report_date': report_data.get('report_date', ''),
                'submitted_by': report_data.get('submitted_by', ''),
                'weather': report_data.get('weather', ''),
                'crew_size': report_data.get('crew_size', 0),
                'work_performed': report_data.get('work_performed', '')[:200] + '...',
                'platform_url': self._get_platform_url()
            }
            
            return self._send_templated_email(
                'daily_report_submitted',
                recipients,
                template_data
            )
            
        except Exception as e:
            logger.error(f"Error sending daily report notification: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def send_inspection_notification(self, inspection_data: Dict, recipients: List[str]) -> Dict:
        """Send notification for inspection completion."""
        try:
            status_colors = {
                'Passed': '#28A745',
                'Failed': '#DC3545', 
                'Conditional Pass': '#FFC107',
                'Rework Required': '#FD7E14'
            }
            
            deficiencies_section = ''
            if inspection_data.get('deficiencies_found'):
                deficiencies_section = f'''
                <div style="background: #f8d7da; padding: 15px; border-radius: 5px; margin: 15px 0;">
                    <h4 style="color: #721c24;">Deficiencies Found:</h4>
                    <p>{inspection_data.get('corrective_action', '')}</p>
                </div>
                '''
            
            template_data = {
                'inspection_type': inspection_data.get('inspection_type', ''),
                'project_name': inspection_data.get('project_name', ''),
                'location': inspection_data.get('location', ''),
                'inspector_name': inspection_data.get('inspector_name', ''),
                'final_status': inspection_data.get('final_status', ''),
                'status_color': status_colors.get(inspection_data.get('final_status'), '#6C757D'),
                'inspection_score': inspection_data.get('inspection_score', 0),
                'deficiencies_section': deficiencies_section,
                'platform_url': self._get_platform_url()
            }
            
            return self._send_templated_email(
                'inspection_completed',
                recipients,
                template_data
            )
            
        except Exception as e:
            logger.error(f"Error sending inspection notification: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def send_payment_application_notification(self, payment_data: Dict, recipients: List[str]) -> Dict:
        """Send notification for payment application submission."""
        try:
            template_data = {
                'application_number': payment_data.get('application_number', ''),
                'project_name': payment_data.get('project_name', ''),
                'period_from': payment_data.get('period_from', ''),
                'period_to': payment_data.get('period_to', ''),
                'contract_sum': float(payment_data.get('contract_sum_to_date', 0)),
                'payment_due': float(payment_data.get('payment_due', 0)),
                'platform_url': self._get_platform_url()
            }
            
            return self._send_templated_email(
                'payment_application_submitted',
                recipients,
                template_data
            )
            
        except Exception as e:
            logger.error(f"Error sending payment application notification: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def send_safety_incident_alert(self, incident_data: Dict, recipients: List[str]) -> Dict:
        """Send urgent safety incident alert."""
        try:
            template_data = {
                'project_name': incident_data.get('project_name', ''),
                'incident_date': incident_data.get('incident_date', ''),
                'location': incident_data.get('location', ''),
                'severity': incident_data.get('severity', ''),
                'reported_by': incident_data.get('reported_by', ''),
                'incident_description': incident_data.get('incident_description', ''),
                'platform_url': self._get_platform_url()
            }
            
            # Mark as high priority for safety incidents
            return self._send_templated_email(
                'safety_incident_alert',
                recipients,
                template_data,
                priority='high'
            )
            
        except Exception as e:
            logger.error(f"Error sending safety incident alert: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def _send_templated_email(self, template_name: str, recipients: List[str], 
                            template_data: Dict, priority: str = 'normal') -> Dict:
        """Send email using template with data substitution."""
        try:
            if not self.smtp_username or not self.smtp_password:
                return {
                    'success': False, 
                    'message': 'Email configuration incomplete. Please provide SMTP credentials.'
                }
            
            template = self.templates.get(template_name)
            if not template:
                return {'success': False, 'message': f'Template {template_name} not found'}
            
            # Prepare email content
            subject = template['subject'].format(**template_data)
            
            # Add recipient name to template data for each recipient
            successful_sends = 0
            failed_sends = 0
            
            for recipient in recipients:
                try:
                    # Get recipient name
                    recipient_name = self._get_recipient_name(recipient)
                    template_data['recipient_name'] = recipient_name
                    
                    html_content = template['template'].format(**template_data)
                    
                    # Send email
                    result = self._send_email(recipient, subject, html_content, priority)
                    
                    if result['success']:
                        successful_sends += 1
                        
                        # Log notification
                        self._log_notification(template_name, recipient, subject, 'sent')
                    else:
                        failed_sends += 1
                        self._log_notification(template_name, recipient, subject, 'failed')
                        
                except Exception as e:
                    logger.error(f"Error sending email to {recipient}: {str(e)}")
                    failed_sends += 1
            
            return {
                'success': successful_sends > 0,
                'successful_sends': successful_sends,
                'failed_sends': failed_sends,
                'message': f'Sent {successful_sends} emails, {failed_sends} failed'
            }
            
        except Exception as e:
            logger.error(f"Error in templated email send: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def _send_email(self, to_email: str, subject: str, html_content: str, priority: str = 'normal') -> Dict:
        """Send individual email via SMTP."""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Set priority headers
            if priority == 'high':
                msg['X-Priority'] = '1'
                msg['X-MSMail-Priority'] = 'High'
                msg['Importance'] = 'High'
            
            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}")
            return {'success': True}
            
        except Exception as e:
            logger.error(f"SMTP error sending to {to_email}: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _get_recipient_name(self, email: str) -> str:
        """Get recipient name from database."""
        try:
            user = self.db.execute_query(
                "SELECT full_name FROM users WHERE email = :email",
                {'email': email}
            )
            return user[0]['full_name'] if user else email.split('@')[0].title()
        except:
            return email.split('@')[0].title()
    
    def _get_platform_url(self) -> str:
        """Get platform URL for email links."""
        return os.environ.get('PLATFORM_URL', 'https://your-gcpanel-domain.com')
    
    def _log_notification(self, template_name: str, recipient: str, subject: str, status: str):
        """Log notification delivery for audit trail."""
        try:
            notification_log = {
                'template_name': template_name,
                'recipient': recipient,
                'subject': subject,
                'status': status,
                'sent_by': st.session_state.get('user_id'),
                'sent_at': datetime.utcnow()
            }
            
            self.db.insert_data('notification_log', notification_log)
            
        except Exception as e:
            logger.error(f"Error logging notification: {str(e)}")
    
    def get_notification_stats(self, days: int = 30) -> Dict:
        """Get notification delivery statistics."""
        try:
            query = """
            SELECT 
                template_name,
                status,
                COUNT(*) as count,
                DATE(sent_at) as date
            FROM notification_log 
            WHERE sent_at >= NOW() - INTERVAL :days DAY
            GROUP BY template_name, status, DATE(sent_at)
            ORDER BY date DESC
            """
            
            stats = self.db.execute_query(query, {'days': days})
            return {'stats': stats, 'period_days': days}
            
        except Exception as e:
            logger.error(f"Error getting notification stats: {str(e)}")
            return {}

# Global notification manager instance
notification_manager = None

def get_notification_manager():
    """Get or create notification manager instance."""
    global notification_manager
    if notification_manager is None:
        notification_manager = NotificationManager()
    return notification_manager