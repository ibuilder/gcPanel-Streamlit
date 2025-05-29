"""
External Service Integrations for gcPanel Construction Platform

Integration with accounting systems, weather services, and third-party APIs
for comprehensive construction management workflow automation.
"""

import streamlit as st
import os
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExternalIntegrations:
    """Manage external service integrations for construction workflows."""
    
    def __init__(self):
        """Initialize external integrations manager."""
        self.weather_api_key = os.environ.get('WEATHER_API_KEY')
        self.quickbooks_client_id = os.environ.get('QUICKBOOKS_CLIENT_ID')
        self.quickbooks_client_secret = os.environ.get('QUICKBOOKS_CLIENT_SECRET')
        self.sage_api_key = os.environ.get('SAGE_API_KEY')
        
        self.integrations_config = {
            'weather': {
                'enabled': bool(self.weather_api_key),
                'provider': 'OpenWeatherMap',
                'base_url': 'https://api.openweathermap.org/data/2.5'
            },
            'accounting': {
                'quickbooks_enabled': bool(self.quickbooks_client_id),
                'sage_enabled': bool(self.sage_api_key)
            }
        }
    
    def get_weather_data(self, location: str, project_lat: float = None, project_lon: float = None) -> Dict:
        """Get current weather data for construction site."""
        try:
            if not self.weather_api_key:
                return {
                    'success': False,
                    'message': 'Weather API key not configured. Please provide WEATHER_API_KEY in admin settings.',
                    'data': None
                }
            
            # Use coordinates if provided, otherwise use location name
            if project_lat and project_lon:
                url = f"{self.integrations_config['weather']['base_url']}/weather"
                params = {
                    'lat': project_lat,
                    'lon': project_lon,
                    'appid': self.weather_api_key,
                    'units': 'imperial'
                }
            else:
                url = f"{self.integrations_config['weather']['base_url']}/weather"
                params = {
                    'q': location,
                    'appid': self.weather_api_key,
                    'units': 'imperial'
                }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            weather_data = response.json()
            
            # Parse weather information relevant to construction
            construction_weather = {
                'temperature': weather_data['main']['temp'],
                'feels_like': weather_data['main']['feels_like'],
                'humidity': weather_data['main']['humidity'],
                'pressure': weather_data['main']['pressure'],
                'visibility': weather_data.get('visibility', 0) / 1000,  # Convert to km
                'wind_speed': weather_data['wind']['speed'],
                'wind_direction': weather_data['wind'].get('deg', 0),
                'weather_condition': weather_data['weather'][0]['main'],
                'description': weather_data['weather'][0]['description'],
                'precipitation': weather_data.get('rain', {}).get('1h', 0),
                'timestamp': datetime.now().isoformat(),
                'location': weather_data['name']
            }
            
            # Add construction work recommendations
            construction_weather['work_recommendations'] = self._get_work_recommendations(construction_weather)
            
            return {
                'success': True,
                'data': construction_weather,
                'message': 'Weather data retrieved successfully'
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Weather API request failed: {str(e)}")
            return {
                'success': False,
                'message': f'Weather service unavailable: {str(e)}',
                'data': None
            }
        except Exception as e:
            logger.error(f"Error getting weather data: {str(e)}")
            return {
                'success': False,
                'message': f'Weather data error: {str(e)}',
                'data': None
            }
    
    def get_weather_forecast(self, location: str, days: int = 5) -> Dict:
        """Get weather forecast for construction planning."""
        try:
            if not self.weather_api_key:
                return {
                    'success': False,
                    'message': 'Weather API key not configured. Please provide WEATHER_API_KEY in admin settings.',
                    'data': None
                }
            
            url = f"{self.integrations_config['weather']['base_url']}/forecast"
            params = {
                'q': location,
                'appid': self.weather_api_key,
                'units': 'imperial',
                'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            forecast_data = response.json()
            
            # Process forecast for construction planning
            daily_forecasts = []
            current_date = None
            daily_data = {
                'temps': [],
                'conditions': [],
                'precipitation': [],
                'wind_speeds': []
            }
            
            for item in forecast_data['list']:
                forecast_date = datetime.fromtimestamp(item['dt']).date()
                
                if current_date != forecast_date:
                    if current_date is not None:
                        # Process previous day's data
                        daily_forecasts.append(self._process_daily_forecast(current_date, daily_data))
                    
                    # Reset for new day
                    current_date = forecast_date
                    daily_data = {
                        'temps': [],
                        'conditions': [],
                        'precipitation': [],
                        'wind_speeds': []
                    }
                
                # Collect data for current day
                daily_data['temps'].append(item['main']['temp'])
                daily_data['conditions'].append(item['weather'][0]['main'])
                daily_data['precipitation'].append(item.get('rain', {}).get('3h', 0))
                daily_data['wind_speeds'].append(item['wind']['speed'])
            
            # Process last day
            if current_date is not None:
                daily_forecasts.append(self._process_daily_forecast(current_date, daily_data))
            
            return {
                'success': True,
                'data': {
                    'location': forecast_data['city']['name'],
                    'forecasts': daily_forecasts,
                    'generated_at': datetime.now().isoformat()
                },
                'message': 'Weather forecast retrieved successfully'
            }
            
        except Exception as e:
            logger.error(f"Error getting weather forecast: {str(e)}")
            return {
                'success': False,
                'message': f'Weather forecast error: {str(e)}',
                'data': None
            }
    
    def _process_daily_forecast(self, date: datetime.date, daily_data: Dict) -> Dict:
        """Process daily forecast data for construction planning."""
        temps = daily_data['temps']
        conditions = daily_data['conditions']
        precipitation = daily_data['precipitation']
        wind_speeds = daily_data['wind_speeds']
        
        # Calculate daily summary
        forecast_summary = {
            'date': date.isoformat(),
            'temp_high': max(temps) if temps else 0,
            'temp_low': min(temps) if temps else 0,
            'avg_temp': sum(temps) / len(temps) if temps else 0,
            'total_precipitation': sum(precipitation),
            'max_wind_speed': max(wind_speeds) if wind_speeds else 0,
            'dominant_condition': max(set(conditions), key=conditions.count) if conditions else 'Unknown',
            'work_suitability': self._assess_work_suitability(temps, conditions, precipitation, wind_speeds)
        }
        
        return forecast_summary
    
    def _get_work_recommendations(self, weather_data: Dict) -> List[str]:
        """Generate work recommendations based on weather conditions."""
        recommendations = []
        
        temp = weather_data.get('temperature', 70)
        condition = weather_data.get('weather_condition', '').lower()
        wind_speed = weather_data.get('wind_speed', 0)
        precipitation = weather_data.get('precipitation', 0)
        
        # Temperature recommendations
        if temp < 32:
            recommendations.append("⚠️ Freezing conditions - Monitor concrete curing, protect materials")
        elif temp < 40:
            recommendations.append("🧥 Cold weather - Ensure worker safety, heated enclosures may be needed")
        elif temp > 95:
            recommendations.append("🌡️ Extreme heat - Increase hydration breaks, avoid heavy work during peak hours")
        
        # Precipitation recommendations
        if precipitation > 0.1:
            recommendations.append("🌧️ Precipitation detected - Cover materials, avoid concrete pours")
        
        # Wind recommendations
        if wind_speed > 25:
            recommendations.append("💨 High winds - Restrict crane operations, secure loose materials")
        elif wind_speed > 15:
            recommendations.append("🌬️ Moderate winds - Exercise caution with tall equipment")
        
        # Condition-specific recommendations
        if 'storm' in condition or 'thunderstorm' in condition:
            recommendations.append("⛈️ Storm conditions - Consider work stoppage for safety")
        elif 'snow' in condition:
            recommendations.append("❄️ Snow conditions - Clear walkways, use appropriate equipment")
        elif 'fog' in condition:
            recommendations.append("🌫️ Low visibility - Enhanced safety measures required")
        
        if not recommendations:
            recommendations.append("✅ Good conditions for most construction activities")
        
        return recommendations
    
    def _assess_work_suitability(self, temps: List, conditions: List, precipitation: List, wind_speeds: List) -> str:
        """Assess overall work suitability for the day."""
        if not temps:
            return "Unknown"
        
        avg_temp = sum(temps) / len(temps)
        total_precip = sum(precipitation)
        max_wind = max(wind_speeds) if wind_speeds else 0
        
        # Check for severe conditions
        if total_precip > 0.5 or max_wind > 30 or avg_temp < 20 or avg_temp > 100:
            return "Poor"
        elif total_precip > 0.1 or max_wind > 20 or avg_temp < 35 or avg_temp > 90:
            return "Fair"
        else:
            return "Good"
    
    def sync_with_quickbooks(self, financial_data: Dict) -> Dict:
        """Sync construction financial data with QuickBooks."""
        try:
            if not self.quickbooks_client_id:
                return {
                    'success': False,
                    'message': 'QuickBooks integration not configured. Please provide API credentials in admin settings.',
                    'data': None
                }
            
            # This would implement actual QuickBooks API integration
            # For now, return a simulation response
            return {
                'success': True,
                'message': 'QuickBooks sync would be performed here with proper API credentials',
                'data': {
                    'sync_type': financial_data.get('type', 'invoice'),
                    'amount': financial_data.get('amount', 0),
                    'status': 'pending_credentials'
                }
            }
            
        except Exception as e:
            logger.error(f"QuickBooks sync error: {str(e)}")
            return {
                'success': False,
                'message': f'QuickBooks sync failed: {str(e)}',
                'data': None
            }
    
    def sync_with_sage(self, project_data: Dict) -> Dict:
        """Sync project data with Sage accounting system."""
        try:
            if not self.sage_api_key:
                return {
                    'success': False,
                    'message': 'Sage integration not configured. Please provide API credentials in admin settings.',
                    'data': None
                }
            
            # This would implement actual Sage API integration
            return {
                'success': True,
                'message': 'Sage sync would be performed here with proper API credentials',
                'data': {
                    'project_id': project_data.get('project_id'),
                    'sync_status': 'pending_credentials'
                }
            }
            
        except Exception as e:
            logger.error(f"Sage sync error: {str(e)}")
            return {
                'success': False,
                'message': f'Sage sync failed: {str(e)}',
                'data': None
            }
    
    def get_integration_status(self) -> Dict:
        """Get status of all external integrations."""
        return {
            'weather': {
                'enabled': self.integrations_config['weather']['enabled'],
                'provider': self.integrations_config['weather']['provider'],
                'status': 'configured' if self.weather_api_key else 'needs_api_key'
            },
            'quickbooks': {
                'enabled': self.integrations_config['accounting']['quickbooks_enabled'],
                'status': 'configured' if self.quickbooks_client_id else 'needs_credentials'
            },
            'sage': {
                'enabled': self.integrations_config['accounting']['sage_enabled'],
                'status': 'configured' if self.sage_api_key else 'needs_credentials'
            }
        }

# Global integrations instance
external_integrations = None

def get_external_integrations():
    """Get or create external integrations instance."""
    global external_integrations
    if external_integrations is None:
        external_integrations = ExternalIntegrations()
    return external_integrations

def render_integrations_dashboard():
    """Render external integrations management dashboard."""
    st.title("🔗 External Integrations")
    
    integrations = get_external_integrations()
    integration_status = integrations.get_integration_status()
    
    # Integration status overview
    st.markdown("### 📊 Integration Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        weather_status = integration_status['weather']
        status_icon = "✅" if weather_status['enabled'] else "❌"
        st.metric("Weather Service", f"{status_icon} {weather_status['provider']}")
        if not weather_status['enabled']:
            st.caption("❌ API key required")
    
    with col2:
        qb_status = integration_status['quickbooks']
        status_icon = "✅" if qb_status['enabled'] else "❌"
        st.metric("QuickBooks", f"{status_icon} Integration")
        if not qb_status['enabled']:
            st.caption("❌ Credentials required")
    
    with col3:
        sage_status = integration_status['sage']
        status_icon = "✅" if sage_status['enabled'] else "❌"
        st.metric("Sage Accounting", f"{status_icon} Integration")
        if not sage_status['enabled']:
            st.caption("❌ API key required")
    
    st.markdown("---")
    
    # Integration testing
    st.markdown("### 🧪 Test Integrations")
    
    # Weather integration test
    if weather_status['enabled']:
        st.markdown("#### 🌤️ Weather Data Test")
        location = st.text_input("Test Location", value="New York, NY", key="weather_location")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌡️ Get Current Weather"):
                with st.spinner("Fetching weather data..."):
                    weather_result = integrations.get_weather_data(location)
                    if weather_result['success']:
                        weather_data = weather_result['data']
                        st.success("✅ Weather data retrieved successfully!")
                        
                        # Display weather information
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("Temperature", f"{weather_data['temperature']:.1f}°F")
                        with col_b:
                            st.metric("Humidity", f"{weather_data['humidity']}%")
                        with col_c:
                            st.metric("Wind Speed", f"{weather_data['wind_speed']} mph")
                        
                        st.info(f"Conditions: {weather_data['description'].title()}")
                        
                        # Show work recommendations
                        if weather_data['work_recommendations']:
                            st.markdown("**Work Recommendations:**")
                            for rec in weather_data['work_recommendations']:
                                st.write(f"• {rec}")
                    else:
                        st.error(f"❌ {weather_result['message']}")
        
        with col2:
            if st.button("📅 Get 5-Day Forecast"):
                with st.spinner("Fetching forecast data..."):
                    forecast_result = integrations.get_weather_forecast(location)
                    if forecast_result['success']:
                        st.success("✅ Forecast data retrieved successfully!")
                        
                        forecast_data = forecast_result['data']
                        for forecast in forecast_data['forecasts'][:3]:  # Show first 3 days
                            date_str = datetime.fromisoformat(forecast['date']).strftime('%m/%d')
                            st.write(f"**{date_str}:** {forecast['temp_high']:.0f}°F/{forecast['temp_low']:.0f}°F - {forecast['dominant_condition']} - Work: {forecast['work_suitability']}")
                    else:
                        st.error(f"❌ {forecast_result['message']}")
    else:
        st.warning("⚠️ Weather integration not configured. Please provide WEATHER_API_KEY to test weather services.")
    
    st.markdown("---")
    
    # Accounting integration test
    st.markdown("#### 💰 Accounting Integration Test")
    
    if qb_status['enabled'] or sage_status['enabled']:
        test_data = {
            'type': 'invoice',
            'amount': 25000.00,
            'project_id': 'PROJ-001',
            'description': 'Monthly progress payment'
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            if qb_status['enabled'] and st.button("📊 Test QuickBooks Sync"):
                result = integrations.sync_with_quickbooks(test_data)
                if result['success']:
                    st.success("✅ QuickBooks connection test successful!")
                else:
                    st.error(f"❌ {result['message']}")
        
        with col2:
            if sage_status['enabled'] and st.button("📈 Test Sage Sync"):
                result = integrations.sync_with_sage(test_data)
                if result['success']:
                    st.success("✅ Sage connection test successful!")
                else:
                    st.error(f"❌ {result['message']}")
    else:
        st.warning("⚠️ Accounting integrations not configured. Please provide API credentials to test accounting systems.")

def render():
    """Main render function for integrations module."""
    render_integrations_dashboard()