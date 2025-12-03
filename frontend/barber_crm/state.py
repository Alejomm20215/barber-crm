"""Enhanced State Management for Barbershop CRM"""

import reflex as rx
import httpx
import os
from typing import List, Optional

# API URL - can be overridden via environment variable
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000/api")


class Business(rx.Base):
    id: str
    name: str
    address: str = ""
    phone: str = ""


class Customer(rx.Base):
    id: str
    name: str
    email: str = ""
    phone: str = ""
    total_visits: int = 0


class Staff(rx.Base):
    id: str
    name: str
    email: str = ""
    phone: str = ""
    role: str = "Barber"


class Service(rx.Base):
    id: str
    name: str
    description: str = ""
    price: float = 0.0
    duration: int = 30


class Appointment(rx.Base):
    id: str
    customer_name: str = ""
    staff_name: str = ""
    service_name: str = ""
    scheduled_at: str = ""
    status: str = "scheduled"
    customer_id: str = ""
    staff_id: str = ""
    service_id: str = ""


class AppState(rx.State):
    """Global application state"""
    
    api_url: str = API_BASE_URL
    is_authenticated: bool = True
    current_user: str = "admin"
    
    # Current selections
    selected_business_id: Optional[str] = None
    selected_business_name: str = "Select Business"
    
    # Data lists
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
    
    # ============ MODAL STATES ============
    show_customer_modal: bool = False
    show_staff_modal: bool = False
    show_service_modal: bool = False
    show_appointment_modal: bool = False
    
    # ============ FORM FIELDS ============
    # Customer form
    form_customer_name: str = ""
    form_customer_email: str = ""
    form_customer_phone: str = ""
    
    # Staff form
    form_staff_name: str = ""
    form_staff_email: str = ""
    form_staff_phone: str = ""
    form_staff_role: str = "Barber"
    
    # Service form
    form_service_name: str = ""
    form_service_description: str = ""
    form_service_price: str = ""
    form_service_duration: str = "30"
    
    # Appointment form
    form_appt_customer: str = ""
    form_appt_staff: str = ""
    form_appt_service: str = ""
    form_appt_date: str = ""
    form_appt_time: str = ""
    
    # ============ TOGGLE MODALS ============
    def toggle_customer_modal(self):
        self.show_customer_modal = not self.show_customer_modal
        if not self.show_customer_modal:
            self._reset_customer_form()
    
    def toggle_staff_modal(self):
        self.show_staff_modal = not self.show_staff_modal
        if not self.show_staff_modal:
            self._reset_staff_form()
    
    def toggle_service_modal(self):
        self.show_service_modal = not self.show_service_modal
        if not self.show_service_modal:
            self._reset_service_form()
    
    def toggle_appointment_modal(self):
        self.show_appointment_modal = not self.show_appointment_modal
        if not self.show_appointment_modal:
            self._reset_appointment_form()
    
    # ============ RESET FORMS ============
    def _reset_customer_form(self):
        self.form_customer_name = ""
        self.form_customer_email = ""
        self.form_customer_phone = ""
    
    def _reset_staff_form(self):
        self.form_staff_name = ""
        self.form_staff_email = ""
        self.form_staff_phone = ""
        self.form_staff_role = "Barber"
    
    def _reset_service_form(self):
        self.form_service_name = ""
        self.form_service_description = ""
        self.form_service_price = ""
        self.form_service_duration = "30"
    
    def _reset_appointment_form(self):
        self.form_appt_customer = ""
        self.form_appt_staff = ""
        self.form_appt_service = ""
        self.form_appt_date = ""
        self.form_appt_time = ""
    
    def clear_messages(self):
        self.error_message = ""
        self.success_message = ""
    
    # ============ LOAD DATA ============
    async def load_businesses(self):
        self.is_loading = True
        self.error_message = ""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}/businesses/", timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    items = data.get('results', data) if isinstance(data, dict) else data
                    self.businesses = [Business(**item) for item in items]
                    if not self.selected_business_id and self.businesses:
                        self.selected_business_id = self.businesses[0].id
                        self.selected_business_name = self.businesses[0].name
                        await self.load_business_data()
        except Exception as e:
            self.error_message = f"Connection error: {str(e)}"
        finally:
            self.is_loading = False
    
    def select_business(self, business_id: str, business_name: str):
        self.selected_business_id = business_id
        self.selected_business_name = business_name
        return AppState.load_business_data
    
    async def load_business_data(self):
        if not self.selected_business_id:
            return
        self.is_loading = True
        try:
            async with httpx.AsyncClient() as client:
                # Load customers
                resp = await client.get(f"{self.api_url}/customers/", params={"business": self.selected_business_id}, timeout=10.0)
                if resp.status_code == 200:
                    data = resp.json()
                    items = data.get('results', data) if isinstance(data, dict) else data
                    self.customers = [Customer(**item) for item in items]
                    self.total_customers = len(self.customers)
                
                # Load staff
                resp = await client.get(f"{self.api_url}/staff/", params={"business": self.selected_business_id}, timeout=10.0)
                if resp.status_code == 200:
                    data = resp.json()
                    items = data.get('results', data) if isinstance(data, dict) else data
                    self.staff = [Staff(**item) for item in items]
                    self.total_staff = len(self.staff)
                
                # Load services
                resp = await client.get(f"{self.api_url}/services/", params={"business": self.selected_business_id}, timeout=10.0)
                if resp.status_code == 200:
                    data = resp.json()
                    items = data.get('results', data) if isinstance(data, dict) else data
                    self.services = [Service(**item) for item in items]
                    self.total_services = len(self.services)
                
                # Load appointments
                resp = await client.get(f"{self.api_url}/appointments/", params={"business": self.selected_business_id}, timeout=10.0)
                if resp.status_code == 200:
                    data = resp.json()
                    items = data.get('results', data) if isinstance(data, dict) else data
                    self.appointments = [Appointment(**item) for item in items]
                    self.total_appointments = len(self.appointments)
        except Exception as e:
            self.error_message = f"Error loading data: {str(e)}"
        finally:
            self.is_loading = False
    
    # ============ CREATE CUSTOMER ============
    async def create_customer(self):
        if not self.form_customer_name:
            self.error_message = "Customer name is required"
            return
        
        self.is_loading = True
        try:
            payload = {
                "business": self.selected_business_id,
                "name": self.form_customer_name,
                "email": self.form_customer_email,
                "phone": self.form_customer_phone,
            }
            async with httpx.AsyncClient() as client:
                resp = await client.post(f"{self.api_url}/customers/", json=payload, timeout=10.0)
                if resp.status_code == 201:
                    self.success_message = "Customer added successfully!"
                    self.show_customer_modal = False
                    self._reset_customer_form()
                    await self.load_business_data()
                else:
                    self.error_message = f"Error: {resp.text}"
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
        finally:
            self.is_loading = False
    
    # ============ CREATE STAFF ============
    async def create_staff(self):
        if not self.form_staff_name:
            self.error_message = "Staff name is required"
            return
        
        self.is_loading = True
        try:
            payload = {
                "business": self.selected_business_id,
                "name": self.form_staff_name,
                "email": self.form_staff_email,
                "phone": self.form_staff_phone,
                "role": self.form_staff_role,
            }
            async with httpx.AsyncClient() as client:
                resp = await client.post(f"{self.api_url}/staff/", json=payload, timeout=10.0)
                if resp.status_code == 201:
                    self.success_message = "Staff member added!"
                    self.show_staff_modal = False
                    self._reset_staff_form()
                    await self.load_business_data()
                else:
                    self.error_message = f"Error: {resp.text}"
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
        finally:
            self.is_loading = False
    
    # ============ CREATE SERVICE ============
    async def create_service(self):
        if not self.form_service_name or not self.form_service_price:
            self.error_message = "Service name and price are required"
            return
        
        self.is_loading = True
        try:
            payload = {
                "business": self.selected_business_id,
                "name": self.form_service_name,
                "description": self.form_service_description,
                "price": float(self.form_service_price),
                "duration": int(self.form_service_duration) if self.form_service_duration else 30,
            }
            async with httpx.AsyncClient() as client:
                resp = await client.post(f"{self.api_url}/services/", json=payload, timeout=10.0)
                if resp.status_code == 201:
                    self.success_message = "Service added!"
                    self.show_service_modal = False
                    self._reset_service_form()
                    await self.load_business_data()
                else:
                    self.error_message = f"Error: {resp.text}"
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
        finally:
            self.is_loading = False
    
    # ============ CREATE APPOINTMENT ============
    async def create_appointment(self):
        if not all([self.form_appt_customer, self.form_appt_staff, self.form_appt_service, self.form_appt_date, self.form_appt_time]):
            self.error_message = "All fields are required"
            return
        
        self.is_loading = True
        try:
            scheduled_at = f"{self.form_appt_date}T{self.form_appt_time}:00"
            payload = {
                "business": self.selected_business_id,
                "customer": self.form_appt_customer,
                "staff": self.form_appt_staff,
                "service": self.form_appt_service,
                "scheduled_at": scheduled_at,
                "status": "scheduled"
            }
            async with httpx.AsyncClient() as client:
                resp = await client.post(f"{self.api_url}/appointments/", json=payload, timeout=10.0)
                if resp.status_code == 201:
                    self.success_message = "Appointment booked!"
                    self.show_appointment_modal = False
                    self._reset_appointment_form()
                    await self.load_business_data()
                else:
                    self.error_message = f"Error: {resp.text}"
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
        finally:
            self.is_loading = False
    
    # ============ DELETE OPERATIONS ============
    async def delete_customer(self, customer_id: str):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.delete(f"{self.api_url}/customers/{customer_id}/", timeout=10.0)
                if resp.status_code == 204:
                    self.success_message = "Customer deleted"
                    await self.load_business_data()
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
    
    async def delete_staff(self, staff_id: str):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.delete(f"{self.api_url}/staff/{staff_id}/", timeout=10.0)
                if resp.status_code == 204:
                    self.success_message = "Staff member deleted"
                    await self.load_business_data()
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
    
    async def delete_service(self, service_id: str):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.delete(f"{self.api_url}/services/{service_id}/", timeout=10.0)
                if resp.status_code == 204:
                    self.success_message = "Service deleted"
                    await self.load_business_data()
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
    
    async def delete_appointment(self, appt_id: str):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.delete(f"{self.api_url}/appointments/{appt_id}/", timeout=10.0)
                if resp.status_code == 204:
                    self.success_message = "Appointment cancelled"
                    await self.load_business_data()
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
