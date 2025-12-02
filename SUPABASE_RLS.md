# Supabase RLS Policies

## Enable RLS on all tables

```sql
ALTER TABLE businesses ENABLE ROW LEVEL SECURITY;
ALTER TABLE staff ENABLE ROW LEVEL SECURITY;
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE services ENABLE ROW LEVEL SECURITY;
ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;
```

## Businesses Table Policies

```sql
-- SELECT policy
CREATE POLICY "users_can_view_own_businesses" 
ON businesses 
FOR SELECT 
USING (owner_user_id = auth.uid());

-- INSERT policy
CREATE POLICY "users_can_create_businesses" 
ON businesses 
FOR INSERT 
WITH CHECK (owner_user_id = auth.uid());

-- UPDATE policy
CREATE POLICY "users_can_update_own_businesses" 
ON businesses 
FOR UPDATE 
USING (owner_user_id = auth.uid());

-- DELETE policy
CREATE POLICY "users_can_delete_own_businesses" 
ON businesses 
FOR DELETE 
USING (owner_user_id = auth.uid());
```

## Staff Table Policies

```sql
-- SELECT policy
CREATE POLICY "business_can_view_own_staff" 
ON staff 
FOR SELECT 
USING (
  business_id IN (
    SELECT id FROM businesses WHERE owner_user_id = auth.uid()
  )
);

-- INSERT policy
CREATE POLICY "business_can_create_staff" 
ON staff 
FOR INSERT 
WITH CHECK (
  business_id IN (
    SELECT id FROM businesses WHERE owner_user_id = auth.uid()
  )
);

-- UPDATE policy
CREATE POLICY "business_can_update_own_staff" 
ON staff 
FOR UPDATE 
USING (
  business_id IN (
    SELECT id FROM businesses WHERE owner_user_id = auth.uid()
  )
);

-- DELETE policy
CREATE POLICY "business_can_delete_own_staff" 
ON staff 
FOR DELETE 
USING (
  business_id IN (
    SELECT id FROM businesses WHERE owner_user_id = auth.uid()
  )
);
```

## Customers Table Policies

```sql
-- SELECT policy
CREATE POLICY "business_can_view_own_customers" 
ON customers 
FOR SELECT 
USING (
  business_id IN (
    SELECT id FROM businesses WHERE owner_user_id = auth.uid()
  )
);

-- INSERT policy
CREATE POLICY "business_can_create_customers" 
ON customers 
FOR INSERT 
WITH CHECK (
  business_id IN (
    SELECT id FROM businesses WHERE owner_user_id = auth.uid()
  )
);

-- UPDATE policy
CREATE POLICY "business_can_update_own_customers" 
ON customers 
FOR UPDATE 
USING (
  business_id IN (
    SELECT id FROM businesses WHERE owner_user_id = auth.uid()
  )
);

-- DELETE policy
CREATE POLICY "business_can_delete_own_customers" 
ON customers 
FOR DELETE 
USING (
  business_id IN (
    SELECT id FROM businesses WHERE owner_user_id = auth.uid()
  )
);
```

## Services Table Policies

```sql
-- SELECT policy
CREATE POLICY "business_can_view_own_services" 
ON services 
FOR SELECT 
USING (
  business_id IN (
    SELECT id FROM businesses WHERE owner_user_id = auth.uid()
  )
);

-- INSERT policy
CREATE POLICY "business_can_create_services" 
ON services 
FOR INSERT 
WITH CHECK (
  business_id IN (
    SELECT id FROM businesses WHERE owner_user_id = auth.uid()
  )
);

-- UPDATE policy
CREATE POLICY "business_can_update_own_services" 
ON services 
FOR UPDATE 
USING (
  business_id IN (
    SELECT id FROM businesses WHERE owner_user_id = auth.uid()
  )
);

-- DELETE policy
CREATE POLICY "business_can_delete_own_services" 
ON services 
FOR DELETE 
USING (
  business_id IN (
    SELECT id FROM businesses WHERE owner_user_id = auth.uid()
  )
);
```

## Appointments Table Policies

```sql
-- SELECT policy
CREATE POLICY "business_can_view_own_appointments" 
ON appointments 
FOR SELECT 
USING (
  business_id IN (
    SELECT id FROM businesses WHERE owner_user_id = auth.uid()
  )
);

-- INSERT policy
CREATE POLICY "business_can_create_appointments" 
ON appointments 
FOR INSERT 
WITH CHECK (
  business_id IN (
    SELECT id FROM businesses WHERE owner_user_id = auth.uid()
  )
);

-- UPDATE policy
CREATE POLICY "business_can_update_own_appointments" 
ON appointments 
FOR UPDATE 
USING (
  business_id IN (
    SELECT id FROM businesses WHERE owner_user_id = auth.uid()
  )
);

-- DELETE policy
CREATE POLICY "business_can_delete_own_appointments" 
ON appointments 
FOR DELETE 
USING (
  business_id IN (
    SELECT id FROM businesses WHERE owner_user_id = auth.uid()
  )
);
```

## Apply All Policies

Run all the above SQL commands in your Supabase SQL editor to enable complete multi-tenant isolation with Row Level Security.

## Testing RLS

After applying policies, test with:

```sql
-- Should only return businesses owned by the authenticated user
SELECT * FROM businesses;

-- Should only return customers for businesses owned by the authenticated user
SELECT * FROM customers;
```
