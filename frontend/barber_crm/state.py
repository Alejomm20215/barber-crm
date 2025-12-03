"""Enhanced State Management for Barbershop CRM"""

import reflex as rx
import httpx
import os
from typing import List, Dict, Optional

# API URL - can be overridden via environment variable
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000/api")


class Business(rx.Base):
    id: str  # UUID from backend
    name: str
    address: str = ""
    phone: str = ""

class Customer(rx.Base):
    id: str  # UUID from backend
    name: str
    email: str = ""
    phone: str = ""
    total_visits: int = 0

class Staff(rx.Base):
    id: str  # UUID from backend
    name: str
    email: str = ""
    phone: str = ""
    role: str = "Staff"

class Service(rx.Base):
    id: str  # UUID from backend
    name: str
    description: str = ""
    price: float = 0.0
    duration: int = 30

class Appointment(rx.Base):
    id: str  # UUID from backend
    customer_name: str = ""
    staff_name: str = ""
    service_name: str = ""
    scheduled_at: str = ""
    status: str = "scheduled"
    # Add fields for IDs if needed for logic, though UI mostly uses names
    customer_id: str = ""  # UUID
    staff_id: str = ""  # UUID
    service_id: str = ""  # UUID

class AppState(rx.State):
    """Global application state"""
    
    # API Configuration - uses environment variable or defaults to localhost
    api_url: str = API_BASE_URL
    
    # Authentication (simplified for now)
    is_authenticated: bool = True
    current_user: str = "admin"
    
    # Current selections
    selected_business_id: Optional[str] = None  # UUID from backend
    selected_business_name: str = "Select a Business"
    
    # Data
    businesses: List[Business] = []
    customers: List[Customer] = []
    staff: List[Staff] = []
    services: List[Service] = []
    appointments: List[Appointment] = []
    
    # UI State
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""
    
    # Stats
    total_customers: int = 0
    total_appointments: int = 0
    total_staff: int = 0
    total_services: int = 0
    
    async def load_businesses(self):
        """Load all businesses"""
        self.is_loading = True
        self.error_message = ""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_url}/businesses/",
                    timeout=10.0
                )
                print(f"[DEBUG] Response status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"[DEBUG] Raw data type: {type(data)}")
                    print(f"[DEBUG] Raw data: {data}")
                    # Handle paginated response
                    if isinstance(data, dict) and 'results' in data:
                        items = data['results']
                        print(f"[DEBUG] Using paginated results: {len(items)} items")
                    else:
                        items = data
                        print(f"[DEBUG] Using direct data: {len(items)} items")
                    self.businesses = [Business(**item) for item in items]
                    print(f"[DEBUG] Created {len(self.businesses)} Business objects")
                    # Auto-select first business if none selected
                    if not self.selected_business_id and self.businesses:
                        self.selected_business_id = self.businesses[0].id
                        self.selected_business_name = self.businesses[0].name
                        print(f"[DEBUG] Auto-selected business: {self.selected_business_name}")
                        # Load data for the first business
                        await self.load_business_data()
                else:
                    self.error_message = f"Error loading businesses: {response.status_code}"
                    print(f"[DEBUG] Error: {self.error_message}")
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
            print(f"[DEBUG] Exception: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.is_loading = False
    
    def select_business(self, business_id: str, business_name: str):
        """Select a business and load its data"""
        self.selected_business_id = business_id
        self.selected_business_name = business_name
        return AppState.load_business_data
    
    async def load_business_data(self):
        """Load data for selected business"""
        if not self.selected_business_id:
            return
        
        self.is_loading = True
        try:
            async with httpx.AsyncClient() as client:
                # Load customers
                response = await client.get(
                    f"{self.api_url}/customers/",
                    params={"business": self.selected_business_id},
                    timeout=10.0
                )
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, dict) and 'results' in data:
                        items = data['results']
                    else:
                        items = data
                    self.customers = [Customer(**item) for item in items]
                    self.total_customers = len(self.customers)
                
                # Load staff
                response = await client.get(
                    f"{self.api_url}/staff/",
                    params={"business": self.selected_business_id},
                    timeout=10.0
                )
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, dict) and 'results' in data:
                        items = data['results']
                    else:
                        items = data
                    self.staff = [Staff(**item) for item in items]
                    self.total_staff = len(self.staff)
                
                # Load services
                response = await client.get(
                    f"{self.api_url}/services/",
                    params={"business": self.selected_business_id},
                    timeout=10.0
                )
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, dict) and 'results' in data:
                        items = data['results']
                    else:
                        items = data
                    self.services = [Service(**item) for item in items]
                    self.total_services = len(self.services)
                
                # Load appointments
                response = await client.get(
                    f"{self.api_url}/appointments/",
                    params={"business": self.selected_business_id},
                    timeout=10.0
                )
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, dict) and 'results' in data:
                        items = data['results']
                    else:
                        items = data
                    self.appointments = [Appointment(**item) for item in items]
                    self.total_appointments = len(self.appointments)
                    
        except Exception as e:
            self.error_message = f"Error loading data: {str(e)}"
        finally:
            self.is_loading = False
    
    # Form State
    new_appointment_customer: str = ""
    new_appointment_staff: str = ""
    new_appointment_service: str = ""
    new_appointment_date: str = ""
    new_appointment_time: str = ""
    is_appointment_modal_open: bool = False

    def toggle_appointment_modal(self):
        """Toggle the new appointment modal"""
        self.is_appointment_modal_open = not self.is_appointment_modal_open

    async def create_appointment(self):
        """Create a new appointment"""
        if not all([self.new_appointment_customer, self.new_appointment_staff, self.new_appointment_service, self.new_appointment_date, self.new_appointment_time]):
            self.error_message = "Please fill in all fields"
            return

        self.is_loading = True
        try:
            # Combine date and time
            scheduled_at = f"{self.new_appointment_date}T{self.new_appointment_time}:00"
            
            payload = {
                "business": self.selected_business_id,
                "customer": self.new_appointment_customer,  # UUID string
                "staff": self.new_appointment_staff,  # UUID string
                "service": self.new_appointment_service,  # UUID string
                "scheduled_at": scheduled_at,
                "status": "scheduled"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/appointments/",
                    json=payload,
                    timeout=10.0
                )
                
                if response.status_code == 201:
                    self.success_message = "Appointment created successfully!"
                    self.is_appointment_modal_open = False
                    # Reset form
                    self.new_appointment_customer = ""
                    self.new_appointment_staff = ""
                    self.new_appointment_service = ""
                    self.new_appointment_date = ""
                    self.new_appointment_time = ""
                    # Reload data
                    await self.load_business_data()
                else:
                    self.error_message = f"Failed to create appointment: {response.text}"
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
        finally:
            self.is_loading = False

    def clear_messages(self):
        """Clear error and success messages"""
        self.error_message = ""
        self.success_message = ""
