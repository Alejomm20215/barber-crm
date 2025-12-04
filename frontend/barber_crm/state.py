"""Enhanced State Management for Barbershop CRM"""

import os
import uuid
from datetime import datetime

import httpx
import reflex as rx
from pydantic import BaseModel

# API URL - can be overridden via environment variable
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000/api")


# ============ DATA MODELS ============
class Business(BaseModel):
    id: str = ""
    name: str = ""
    address: str = ""
    phone: str = ""


class Customer(BaseModel):
    id: str = ""
    name: str = ""
    email: str = ""
    phone: str = ""
    total_visits: int = 0


class Staff(BaseModel):
    id: str = ""
    name: str = ""
    email: str = ""
    phone: str = ""
    role: str = "Barber"


class Service(BaseModel):
    id: str = ""
    name: str = ""
    description: str = ""
    price: float = 0.0
    duration: int = 30


class Appointment(BaseModel):
    id: str = ""
    customer_name: str = ""
    staff_name: str = ""
    service_name: str = ""
    scheduled_at: str = ""
    status: str = "scheduled"
    customer_id: str = ""
    staff_id: str = ""
    service_id: str = ""


class UserProfile(BaseModel):
    id: int = 0
    username: str = ""
    email: str = ""
    first_name: str = ""
    last_name: str = ""
    is_master: bool = False


# ============ AUTH STATE ============
class AuthState(rx.State):
    """Authentication state management."""
    
    # Auth tokens
    access_token: str = ""
    refresh_token: str = ""
    
    # User info
    user: UserProfile = UserProfile()
    is_authenticated: bool = False
    is_master: bool = False
    
    # UI state
    auth_loading: bool = False
    auth_error: str = ""
    
    # Form fields
    login_username: str = ""
    login_password: str = ""
    register_username: str = ""
    register_email: str = ""
    register_password: str = ""
    register_password2: str = ""
    register_first_name: str = ""
    register_last_name: str = ""
    register_phone: str = ""
    
    @rx.var
    def auth_headers(self) -> dict:
        """Get authorization headers for API calls."""
        if self.access_token:
            return {"Authorization": f"Bearer {self.access_token}"}
        return {}
    
    def clear_auth_error(self):
        self.auth_error = ""
    
    def _reset_login_form(self):
        self.login_username = ""
        self.login_password = ""
    
    def _reset_register_form(self):
        self.register_username = ""
        self.register_email = ""
        self.register_password = ""
        self.register_password2 = ""
        self.register_first_name = ""
        self.register_last_name = ""
        self.register_phone = ""
    
    async def login(self):
        """Login with username and password."""
        if not self.login_username or not self.login_password:
            self.auth_error = "Username and password are required"
            return
        
        self.auth_loading = True
        self.auth_error = ""
        
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{API_BASE_URL}/auth/login/",
                    json={
                        "username": self.login_username,
                        "password": self.login_password,
                    },
                    timeout=10.0,
                )
                
                if resp.status_code == 200:
                    data = resp.json()
                    self.access_token = data.get("access", "")
                    self.refresh_token = data.get("refresh", "")
                    
                    user_data = data.get("user", {})
                    self.user = UserProfile(**user_data)
                    self.is_authenticated = True
                    self.is_master = user_data.get("is_master", False)
                    
                    self._reset_login_form()
                    return rx.redirect("/dashboard")
                else:
                    error_data = resp.json()
                    self.auth_error = error_data.get("detail", "Invalid credentials")
        except Exception as e:
            self.auth_error = f"Connection error: {e!s}"
        finally:
            self.auth_loading = False
    
    async def register(self):
        """Register a new user."""
        if not all([self.register_username, self.register_email, self.register_password]):
            self.auth_error = "Username, email and password are required"
            return
        
        if self.register_password != self.register_password2:
            self.auth_error = "Passwords don't match"
            return
        
        self.auth_loading = True
        self.auth_error = ""
        
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{API_BASE_URL}/auth/register/",
                    json={
                        "username": self.register_username,
                        "email": self.register_email,
                        "password": self.register_password,
                        "password2": self.register_password2,
                        "first_name": self.register_first_name,
                        "last_name": self.register_last_name,
                        "phone": self.register_phone,
                    },
                    timeout=10.0,
                )
                
                if resp.status_code == 201:
                    data = resp.json()
                    self.access_token = data.get("access", "")
                    self.refresh_token = data.get("refresh", "")
                    
                    user_data = data.get("user", {})
                    self.user = UserProfile(**user_data)
                    self.is_authenticated = True
                    self.is_master = user_data.get("is_master", False)
                    
                    self._reset_register_form()
                    return rx.redirect("/dashboard")
                else:
                    error_data = resp.json()
                    # Extract first error message
                    if isinstance(error_data, dict):
                        for key, value in error_data.items():
                            if isinstance(value, list):
                                self.auth_error = f"{key}: {value[0]}"
                                break
                            else:
                                self.auth_error = str(value)
                                break
                    else:
                        self.auth_error = "Registration failed"
        except Exception as e:
            self.auth_error = f"Connection error: {e!s}"
        finally:
            self.auth_loading = False
    
    def logout(self):
        """Logout and clear tokens."""
        self.access_token = ""
        self.refresh_token = ""
        self.user = UserProfile()
        self.is_authenticated = False
        self.is_master = False
        return rx.redirect("/login")
    
    async def check_auth(self):
        """Check if user is authenticated on page load."""
        if not self.access_token:
            return
        
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{API_BASE_URL}/auth/me/",
                    headers={"Authorization": f"Bearer {self.access_token}"},
                    timeout=10.0,
                )
                
                if resp.status_code == 200:
                    user_data = resp.json()
                    self.user = UserProfile(**user_data)
                    self.is_authenticated = True
                    self.is_master = user_data.get("is_master", False)
                else:
                    # Token expired, try refresh
                    await self.refresh_access_token()
        except Exception:
            self.is_authenticated = False
    
    async def refresh_access_token(self):
        """Refresh the access token."""
        if not self.refresh_token:
            self.is_authenticated = False
            return
        
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{API_BASE_URL}/auth/refresh/",
                    json={"refresh": self.refresh_token},
                    timeout=10.0,
                )
                
                if resp.status_code == 200:
                    data = resp.json()
                    self.access_token = data.get("access", "")
                    if "refresh" in data:
                        self.refresh_token = data["refresh"]
                else:
                    self.logout()
        except Exception:
            self.logout()


# ============ APP STATE ============
class AppState(AuthState):
    """Global application state with optimistic UI updates."""
    
    api_url: str = API_BASE_URL
    current_user: str = "admin"
    
    # Current selections
    selected_business_id: str | None = None
    selected_business_name: str = "Select Business"
    
    # Data lists
    businesses: list[Business] = []
    customers: list[Customer] = []
    staff: list[Staff] = []
    services: list[Service] = []
    appointments: list[Appointment] = []
    
    # UI State
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""
    
    # Optimistic UI - pending operations
    _pending_deletes: list[str] = []
    
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
    form_customer_name: str = ""
    form_customer_email: str = ""
    form_customer_phone: str = ""
    form_staff_name: str = ""
    form_staff_email: str = ""
    form_staff_phone: str = ""
    form_staff_role: str = "Barber"
    form_service_name: str = ""
    form_service_description: str = ""
    form_service_price: str = ""
    form_service_duration: str = "30"
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
            headers = self.auth_headers if self.access_token else {}
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_url}/businesses/",
                    headers=headers,
                    timeout=10.0,
                )
                if response.status_code == 200:
                    data = response.json()
                    items = data.get("results", data) if isinstance(data, dict) else data
                    self.businesses = [Business(**item) for item in items]
                    if not self.selected_business_id and self.businesses:
                        first_biz = self.businesses[0]
                        self.selected_business_id = first_biz.id
                        self.selected_business_name = first_biz.name
                        await self.load_business_data()
        except Exception as e:
            self.error_message = f"Connection error: {e!s}"
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
            headers = self.auth_headers if self.access_token else {}
            async with httpx.AsyncClient() as client:
                # Load customers
                resp = await client.get(
                    f"{self.api_url}/customers/",
                    params={"business": self.selected_business_id},
                    headers=headers,
                    timeout=10.0,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    items = data.get("results", data) if isinstance(data, dict) else data
                    self.customers = [Customer(**item) for item in items]
                    self.total_customers = len(self.customers)
                
                # Load staff
                resp = await client.get(
                    f"{self.api_url}/staff/",
                    params={"business": self.selected_business_id},
                    headers=headers,
                    timeout=10.0,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    items = data.get("results", data) if isinstance(data, dict) else data
                    self.staff = [Staff(**item) for item in items]
                    self.total_staff = len(self.staff)
                
                # Load services
                resp = await client.get(
                    f"{self.api_url}/services/",
                    params={"business": self.selected_business_id},
                    headers=headers,
                    timeout=10.0,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    items = data.get("results", data) if isinstance(data, dict) else data
                    self.services = [Service(**item) for item in items]
                    self.total_services = len(self.services)
                
                # Load appointments
                resp = await client.get(
                    f"{self.api_url}/appointments/",
                    params={"business": self.selected_business_id},
                    headers=headers,
                    timeout=10.0,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    items = data.get("results", data) if isinstance(data, dict) else data
                    self.appointments = [Appointment(**item) for item in items]
                    self.total_appointments = len(self.appointments)
        except Exception as e:
            self.error_message = f"Error loading data: {e!s}"
        finally:
            self.is_loading = False
    
    # ============ OPTIMISTIC CREATE - CUSTOMER ============
    async def create_customer(self):
        if not self.form_customer_name:
            self.error_message = "Customer name is required"
            return
        
        # Create optimistic customer with temp ID
        temp_id = f"temp-{uuid.uuid4()}"
        optimistic_customer = Customer(
            id=temp_id,
            name=self.form_customer_name,
            email=self.form_customer_email,
            phone=self.form_customer_phone,
        )
        
        # Optimistic update - add immediately
        self.customers = [optimistic_customer] + list(self.customers)
        self.total_customers = len(self.customers)
        self.success_message = "Customer added!"
        self.show_customer_modal = False
        
        # Save form data before reset
        payload = {
            "business": self.selected_business_id,
            "name": self.form_customer_name,
            "email": self.form_customer_email,
            "phone": self.form_customer_phone,
        }
        self._reset_customer_form()
        
        # API call in background
        try:
            headers = self.auth_headers if self.access_token else {}
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{self.api_url}/customers/",
                    json=payload,
                    headers=headers,
                    timeout=10.0,
                )
                if resp.status_code == 201:
                    # Replace temp customer with real one
                    real_data = resp.json()
                    self.customers = [
                        Customer(**real_data) if c.id == temp_id else c
                        for c in self.customers
                    ]
                else:
                    # Revert optimistic update
                    self.customers = [c for c in self.customers if c.id != temp_id]
                    self.total_customers = len(self.customers)
                    self.error_message = f"Error: {resp.text}"
        except Exception as e:
            # Revert optimistic update
            self.customers = [c for c in self.customers if c.id != temp_id]
            self.total_customers = len(self.customers)
            self.error_message = f"Error: {e!s}"
    
    # ============ OPTIMISTIC CREATE - STAFF ============
    async def create_staff(self):
        if not self.form_staff_name:
            self.error_message = "Staff name is required"
            return
        
        temp_id = f"temp-{uuid.uuid4()}"
        optimistic_staff = Staff(
            id=temp_id,
            name=self.form_staff_name,
            email=self.form_staff_email,
            phone=self.form_staff_phone,
            role=self.form_staff_role,
        )
        
        # Optimistic update
        self.staff = [optimistic_staff] + list(self.staff)
        self.total_staff = len(self.staff)
        self.success_message = "Staff member added!"
        self.show_staff_modal = False
        
        payload = {
            "business": self.selected_business_id,
            "name": self.form_staff_name,
            "email": self.form_staff_email,
            "phone": self.form_staff_phone,
            "role": self.form_staff_role,
        }
        self._reset_staff_form()
        
        try:
            headers = self.auth_headers if self.access_token else {}
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{self.api_url}/staff/",
                    json=payload,
                    headers=headers,
                    timeout=10.0,
                )
                if resp.status_code == 201:
                    real_data = resp.json()
                    self.staff = [
                        Staff(**real_data) if s.id == temp_id else s
                        for s in self.staff
                    ]
                else:
                    self.staff = [s for s in self.staff if s.id != temp_id]
                    self.total_staff = len(self.staff)
                    self.error_message = f"Error: {resp.text}"
        except Exception as e:
            self.staff = [s for s in self.staff if s.id != temp_id]
            self.total_staff = len(self.staff)
            self.error_message = f"Error: {e!s}"
    
    # ============ OPTIMISTIC CREATE - SERVICE ============
    async def create_service(self):
        if not self.form_service_name or not self.form_service_price:
            self.error_message = "Service name and price are required"
            return
        
        temp_id = f"temp-{uuid.uuid4()}"
        optimistic_service = Service(
            id=temp_id,
            name=self.form_service_name,
            description=self.form_service_description,
            price=float(self.form_service_price),
            duration=int(self.form_service_duration) if self.form_service_duration else 30,
        )
        
        # Optimistic update
        self.services = [optimistic_service] + list(self.services)
        self.total_services = len(self.services)
        self.success_message = "Service added!"
        self.show_service_modal = False
        
        payload = {
            "business": self.selected_business_id,
            "name": self.form_service_name,
            "description": self.form_service_description,
            "price": float(self.form_service_price),
            "duration": int(self.form_service_duration) if self.form_service_duration else 30,
        }
        self._reset_service_form()
        
        try:
            headers = self.auth_headers if self.access_token else {}
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{self.api_url}/services/",
                    json=payload,
                    headers=headers,
                    timeout=10.0,
                )
                if resp.status_code == 201:
                    real_data = resp.json()
                    self.services = [
                        Service(**real_data) if s.id == temp_id else s
                        for s in self.services
                    ]
                else:
                    self.services = [s for s in self.services if s.id != temp_id]
                    self.total_services = len(self.services)
                    self.error_message = f"Error: {resp.text}"
        except Exception as e:
            self.services = [s for s in self.services if s.id != temp_id]
            self.total_services = len(self.services)
            self.error_message = f"Error: {e!s}"
    
    # ============ OPTIMISTIC CREATE - APPOINTMENT ============
    async def create_appointment(self):
        if not all([
            self.form_appt_customer,
            self.form_appt_staff,
            self.form_appt_service,
            self.form_appt_date,
            self.form_appt_time,
        ]):
            self.error_message = "All fields are required"
            return
        
        temp_id = f"temp-{uuid.uuid4()}"
        scheduled_at = f"{self.form_appt_date}T{self.form_appt_time}:00"
        
        # Find names for optimistic display
        customer_name = next((c.name for c in self.customers if c.id == self.form_appt_customer), "Customer")
        staff_name = next((s.name for s in self.staff if s.id == self.form_appt_staff), "Staff")
        service_name = next((s.name for s in self.services if s.id == self.form_appt_service), "Service")
        
        optimistic_appt = Appointment(
            id=temp_id,
            customer_name=customer_name,
            staff_name=staff_name,
            service_name=service_name,
            scheduled_at=scheduled_at,
            status="scheduled",
        )
        
        # Optimistic update
        self.appointments = [optimistic_appt] + list(self.appointments)
        self.total_appointments = len(self.appointments)
        self.success_message = "Appointment booked!"
        self.show_appointment_modal = False
        
        payload = {
            "business": self.selected_business_id,
            "customer": self.form_appt_customer,
            "staff": self.form_appt_staff,
            "service": self.form_appt_service,
            "scheduled_at": scheduled_at,
            "status": "scheduled",
        }
        self._reset_appointment_form()
        
        try:
            headers = self.auth_headers if self.access_token else {}
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{self.api_url}/appointments/",
                    json=payload,
                    headers=headers,
                    timeout=10.0,
                )
                if resp.status_code == 201:
                    real_data = resp.json()
                    self.appointments = [
                        Appointment(**real_data) if a.id == temp_id else a
                        for a in self.appointments
                    ]
                else:
                    self.appointments = [a for a in self.appointments if a.id != temp_id]
                    self.total_appointments = len(self.appointments)
                    self.error_message = f"Error: {resp.text}"
        except Exception as e:
            self.appointments = [a for a in self.appointments if a.id != temp_id]
            self.total_appointments = len(self.appointments)
            self.error_message = f"Error: {e!s}"
    
    # ============ OPTIMISTIC DELETE OPERATIONS ============
    async def delete_customer(self, customer_id: str):
        # Find customer for potential revert
        customer_backup = next((c for c in self.customers if c.id == customer_id), None)
        
        # Optimistic delete - remove immediately
        self.customers = [c for c in self.customers if c.id != customer_id]
        self.total_customers = len(self.customers)
        self.success_message = "Customer deleted"
        
        try:
            headers = self.auth_headers if self.access_token else {}
            async with httpx.AsyncClient() as client:
                resp = await client.delete(
                    f"{self.api_url}/customers/{customer_id}/",
                    headers=headers,
                    timeout=10.0,
                )
                if resp.status_code != 204:
                    # Revert - add back
                    if customer_backup:
                        self.customers = list(self.customers) + [customer_backup]
                        self.total_customers = len(self.customers)
                    self.error_message = "Failed to delete customer"
        except Exception as e:
            # Revert
            if customer_backup:
                self.customers = list(self.customers) + [customer_backup]
                self.total_customers = len(self.customers)
            self.error_message = f"Error: {e!s}"
    
    async def delete_staff(self, staff_id: str):
        staff_backup = next((s for s in self.staff if s.id == staff_id), None)
        
        self.staff = [s for s in self.staff if s.id != staff_id]
        self.total_staff = len(self.staff)
        self.success_message = "Staff member deleted"
        
        try:
            headers = self.auth_headers if self.access_token else {}
            async with httpx.AsyncClient() as client:
                resp = await client.delete(
                    f"{self.api_url}/staff/{staff_id}/",
                    headers=headers,
                    timeout=10.0,
                )
                if resp.status_code != 204 and staff_backup:
                    self.staff = list(self.staff) + [staff_backup]
                    self.total_staff = len(self.staff)
                    self.error_message = "Failed to delete staff member"
        except Exception as e:
            if staff_backup:
                self.staff = list(self.staff) + [staff_backup]
                self.total_staff = len(self.staff)
            self.error_message = f"Error: {e!s}"
    
    async def delete_service(self, service_id: str):
        service_backup = next((s for s in self.services if s.id == service_id), None)
        
        self.services = [s for s in self.services if s.id != service_id]
        self.total_services = len(self.services)
        self.success_message = "Service deleted"
        
        try:
            headers = self.auth_headers if self.access_token else {}
            async with httpx.AsyncClient() as client:
                resp = await client.delete(
                    f"{self.api_url}/services/{service_id}/",
                    headers=headers,
                    timeout=10.0,
                )
                if resp.status_code != 204 and service_backup:
                    self.services = list(self.services) + [service_backup]
                    self.total_services = len(self.services)
                    self.error_message = "Failed to delete service"
        except Exception as e:
            if service_backup:
                self.services = list(self.services) + [service_backup]
                self.total_services = len(self.services)
            self.error_message = f"Error: {e!s}"
    
    async def delete_appointment(self, appt_id: str):
        appt_backup = next((a for a in self.appointments if a.id == appt_id), None)
        
        # Optimistic delete
        self.appointments = [a for a in self.appointments if a.id != appt_id]
        self.total_appointments = len(self.appointments)
        self.success_message = "Appointment cancelled"
        
        try:
            headers = self.auth_headers if self.access_token else {}
            async with httpx.AsyncClient() as client:
                resp = await client.delete(
                    f"{self.api_url}/appointments/{appt_id}/",
                    headers=headers,
                    timeout=10.0,
                )
                if resp.status_code != 204 and appt_backup:
                    self.appointments = list(self.appointments) + [appt_backup]
                    self.total_appointments = len(self.appointments)
                    self.error_message = "Failed to cancel appointment"
        except Exception as e:
            if appt_backup:
                self.appointments = list(self.appointments) + [appt_backup]
                self.total_appointments = len(self.appointments)
            self.error_message = f"Error: {e!s}"
    
    # ============ OPTIMISTIC STATUS UPDATE ============
    async def update_appointment_status(self, appt_id: str, new_status: str):
        """Update appointment status with optimistic UI."""
        # Find and backup
        appt_idx = next((i for i, a in enumerate(self.appointments) if a.id == appt_id), None)
        if appt_idx is None:
            return
        
        old_status = self.appointments[appt_idx].status
        
        # Optimistic update
        updated_appt = self.appointments[appt_idx].model_copy()
        updated_appt.status = new_status
        self.appointments = [
            updated_appt if i == appt_idx else a
            for i, a in enumerate(self.appointments)
        ]
        self.success_message = f"Appointment {new_status}"
        
        try:
            headers = self.auth_headers if self.access_token else {}
            async with httpx.AsyncClient() as client:
                resp = await client.patch(
                    f"{self.api_url}/appointments/{appt_id}/",
                    json={"status": new_status},
                    headers=headers,
                    timeout=10.0,
                )
                if resp.status_code != 200:
                    # Revert
                    reverted_appt = self.appointments[appt_idx].model_copy()
                    reverted_appt.status = old_status
                    self.appointments = [
                        reverted_appt if i == appt_idx else a
                        for i, a in enumerate(self.appointments)
                    ]
                    self.error_message = "Failed to update status"
        except Exception as e:
            # Revert
            reverted_appt = self.appointments[appt_idx].model_copy()
            reverted_appt.status = old_status
            self.appointments = [
                reverted_appt if i == appt_idx else a
                for i, a in enumerate(self.appointments)
            ]
            self.error_message = f"Error: {e!s}"
