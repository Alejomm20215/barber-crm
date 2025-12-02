"""Dashboard State Management"""

import reflex as rx
import httpx
from typing import List, Dict


class DashboardState(rx.State):
    """State for the dashboard"""
    
    # API base URL
    api_url: str = "http://localhost:8000/api"
    
    # Data
    businesses: List[Dict] = []
    staff_members: List[Dict] = []
    customers: List[Dict] = []
    appointments: List[Dict] = []
    services: List[Dict] = []
    
    # Loading states
    is_loading: bool = False
    error_message: str = ""
    
    # Stats
    total_customers: int = 0
    total_appointments: int = 0
    total_staff: int = 0
    
    async def load_dashboard_data(self):
        """Load all dashboard data"""
        self.is_loading = True
        try:
            async with httpx.AsyncClient() as client:
                # Load businesses
                response = await client.get(f"{self.api_url}/businesses/")
                if response.status_code == 200:
                    self.businesses = response.json()
                
                # Load customers
                response = await client.get(f"{self.api_url}/customers/")
                if response.status_code == 200:
                    self.customers = response.json()
                    self.total_customers = len(self.customers)
                
                # Load staff
                response = await client.get(f"{self.api_url}/staff/")
                if response.status_code == 200:
                    self.staff_members = response.json()
                    self.total_staff = len(self.staff_members)
                
                # Load appointments
                response = await client.get(f"{self.api_url}/appointments/")
                if response.status_code == 200:
                    self.appointments = response.json()
                    self.total_appointments = len(self.appointments)
                
                # Load services
                response = await client.get(f"{self.api_url}/services/")
                if response.status_code == 200:
                    self.services = response.json()
                    
        except Exception as e:
            self.error_message = f"Error loading data: {str(e)}"
        finally:
            self.is_loading = False
