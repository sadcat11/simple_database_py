# Task list

## Common
- [ ] Auto-building docs
- [x] Use pydantic for validation
- [ ] Change email validation to pydantic EmailStr

## Server
- [x] Add server-side validation for user data
- [ ] Use asyncio to execute multiple queries in parallel

## Client
- [x] Add checks for user input
- [ ] Transfer user authorization to the client side

## Autotest
- [x] Add autotests for products
- [x] Add tests for new client checks
- [ ] Add tests for new server checks

## Bug
- [x] Fix users and products create with multiple name parts when creates with optional field