# SoftGemZ Website - Backend Integration Contracts

## Contact Form Integration

### Frontend Mock Data to Replace
- **File**: `/app/frontend/src/pages/Contact.jsx`
- **Mock Behavior**: Form submission currently shows success toast and resets form
- **Integration Point**: `handleSubmit` function needs to call actual API

### Backend API Endpoints Required

#### 1. POST /api/contact
**Purpose**: Submit contact form data
**Request Body**:
```json
{
  "name": "string (required)",
  "email": "string (required, valid email)",
  "company": "string (optional)",
  "phone": "string (optional)",
  "projectType": "string (optional)",
  "message": "string (required)"
}
```

**Response Success (201)**:
```json
{
  "success": true,
  "message": "Thank you! We'll get back to you within 24 hours.",
  "id": "contact_submission_id"
}
```

**Response Error (400/500)**:
```json
{
  "success": false,
  "message": "Error message",
  "errors": ["validation errors if any"]
}
```

#### 2. GET /api/contact (Admin)
**Purpose**: Retrieve all contact submissions (for admin view)
**Response**:
```json
{
  "contacts": [
    {
      "id": "string",
      "name": "string",
      "email": "string",
      "company": "string",
      "phone": "string",
      "projectType": "string",
      "message": "string",
      "createdAt": "datetime",
      "status": "new|contacted|resolved"
    }
  ]
}
```

### Database Model

#### ContactSubmission Collection
```javascript
{
  _id: ObjectId,
  name: String (required),
  email: String (required, validated),
  company: String (optional),
  phone: String (optional),
  projectType: String (optional),
  message: String (required),
  status: String (default: "new", enum: ["new", "contacted", "resolved"]),
  createdAt: Date (default: now),
  updatedAt: Date (default: now)
}
```

### Frontend Integration Changes

1. **Remove Mock Submission**: Replace setTimeout mock with actual API call
2. **Add Error Handling**: Handle API errors and show appropriate messages
3. **Loading States**: Show loading spinner during submission
4. **Validation**: Add client-side validation before API call

### Environment Variables
- No new environment variables needed (using existing MONGO_URL)

### Testing Scenarios
1. Valid form submission → Success message
2. Invalid email → Validation error
3. Missing required fields → Validation error
4. Network error → Error handling
5. Server error → Error handling

## Implementation Notes
- Use existing MongoDB connection from server.py
- Follow existing API pattern with /api prefix
- Add proper input validation and sanitization
- Include CORS headers for form submission
- Log contact submissions for monitoring