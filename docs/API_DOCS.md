# API Documentation (Extended)

See live Swagger at `/docs`.

## Auth
- POST `/auth/register` (X-Tenant-ID header) -> creates user and Stripe customer (dev/test)
- POST `/auth/login` -> returns JWT with `role` and `tenant_id` claims

## Patients
- GET/POST /patients (JWT required)
- GET/PUT/DELETE /patients/{id} (JWT required)

## Uploads
- POST /uploads (multipart form: `file`)

## Billing
- POST /billing/create-checkout-session (JWT required) -> returns checkout_url
- POST /billing/webhook -> Stripe webhook endpoint
