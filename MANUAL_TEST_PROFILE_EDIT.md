# Manual Test Plan - Profile Edit Feature

## Prerequisites
1. Backend server running on `http://localhost:8000`
2. Frontend server running on `http://localhost:5173`
3. MongoDB connection active
4. Test user account created

## Test Steps

### Test 1: View Current Profile
1. Login with test credentials
2. Navigate to `/profile`
3. Click "Edit Profile" button
4. **Expected**: Form should load with current username and email

### Test 2: Update Username
1. On profile edit page, change username to a new valid username
2. Click "Save Changes"
3. **Expected**: 
   - Success toast notification appears
   - Redirected or profile data refreshed
   - New username displayed

### Test 3: Update Email
1. On profile edit page, change email to a new valid email
2. Click "Save Changes"
3. **Expected**: 
   - Success toast notification appears
   - Profile updated with new email

### Test 4: Update Both Fields
1. Change both username and email
2. Click "Save Changes"
3. **Expected**: Both fields updated successfully

### Test 5: Validation - Empty Username
1. Clear username field
2. Click "Save Changes"
3. **Expected**: Error message "Username is required"

### Test 6: Validation - Short Username
1. Enter username with less than 3 characters (e.g., "ab")
2. Click "Save Changes"
3. **Expected**: Error message "Username must be at least 3 characters"

### Test 7: Validation - Invalid Username Characters
1. Enter username with special characters (e.g., "test@user")
2. Click "Save Changes"
3. **Expected**: Error message "Username can only contain letters, numbers, and underscores"

### Test 8: Validation - Invalid Email
1. Enter invalid email format (e.g., "notanemail")
2. Click "Save Changes"
3. **Expected**: Error message "Please enter a valid email address"

### Test 9: Duplicate Username
1. Try to change username to one that already exists
2. Click "Save Changes"
3. **Expected**: Error toast with message about username already existing

### Test 10: Duplicate Email
1. Try to change email to one that already exists
2. Click "Save Changes"
3. **Expected**: Error toast with message about email already existing

### Test 11: No Changes
1. Don't modify any field
2. Click "Save Changes"
3. **Expected**: Nothing happens (form doesn't submit)

### Test 12: Cancel Button
1. Make changes to fields
2. Click "Cancel" button
3. **Expected**: Navigate back to profile view without saving changes

### Test 13: Loading State
1. Start profile update (may need slow network to observe)
2. **Expected**: 
   - "Saving..." text appears
   - Button disabled during save
   - Loading spinner visible

### Test 14: Backend Error Handling
1. Stop MongoDB or backend server
2. Try to update profile
3. **Expected**: Error toast with appropriate message

## API Endpoint Test (cURL)

### Update Profile
```bash
# Get token first
TOKEN="your_jwt_token_here"

# Update username
curl -X PUT http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newusername"
  }'

# Update email
curl -X PUT http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newemail@example.com"
  }'

# Update both
curl -X PUT http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newusername",
    "email": "newemail@example.com"
  }'
```

## Success Criteria
- ✅ All frontend validations work correctly
- ✅ Profile updates successfully when valid data provided
- ✅ Appropriate error messages shown for invalid data
- ✅ Loading states display correctly
- ✅ Backend validations prevent duplicate usernames/emails
- ✅ Profile data persists after page refresh
- ✅ Toast notifications appear for success/error cases

