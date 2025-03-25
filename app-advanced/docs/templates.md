# Web Interface with Jinja2 Templates

This guide explains the web interface implemented with Jinja2 templates for the Invoice OCR API.

## Overview

The Invoice OCR API includes a web interface that allows users to interact with the API through their browser. This interface is built using:

- **FastAPI**: Handles HTTP requests and responses
- **Jinja2**: A template engine for rendering HTML templates
- **HTML/CSS**: Provides the structure and styling
- **JavaScript**: Enhances the user experience

## Template Structure

The templates are organized using template inheritance for a consistent look and feel:

1. **base.html**: The base template that defines the common structure and styling
2. **index.html**: The home page
3. **upload.html**: The form for uploading invoices
4. **results.html**: Displays the extraction results
5. **login.html**: The login form
6. **error.html**: Displays error messages

## Routes

The web interface is accessible through the following routes:

- **`/`**: Home page
- **`/web/upload`**: Upload form
- **`/web/process`**: Process uploaded invoice
- **`/web/login`**: Login form
- **`/web/logout`**: Logout endpoint

## Authentication

The web interface uses cookie-based authentication:

1. User submits credentials via the login form
2. Server validates the credentials
3. If valid, a cookie named `auth` is set with the encoded credentials
4. Protected routes check this cookie to verify authentication
5. The logout endpoint clears this cookie

## How Templates Are Rendered

Templates are rendered using the `templates.TemplateResponse()` function from FastAPI:

```python
return templates.TemplateResponse(
    "template_name.html",
    {
        "request": request,  # Required by FastAPI
        "user": user,        # Authentication status
        "other_data": data   # Any other context data
    }
)
```

## Template Syntax

Jinja2 templates use a simple syntax:

- `{% ... %}`: Control structures (if statements, loops, blocks)
- `{{ ... }}`: Variable output
- `{# ... #}`: Comments

Example from our code:

```html
{% extends "base.html" %}

{% block content %}
    <h2>Welcome to the Invoice OCR API</h2>
    
    {% if message %}
        <div class="alert alert-{{ message_type }}">
            {{ message }}
        </div>
    {% endif %}
    
    <!-- More content here -->
{% endblock %}
```

## Template Inheritance

Templates use inheritance to maintain a consistent structure:

1. The `base.html` template defines blocks that can be overridden
2. Child templates extend `base.html` and override specific blocks

Blocks defined in the base template:
- `title`: The page title
- `head`: Additional head content (scripts, styles)
- `content`: The main content area

## Styling

The templates include embedded CSS styles in the `base.html` file for simplicity. In a larger application, you would typically use external CSS files.

The styling uses:
- CSS variables for consistent colors and values
- Responsive design principles
- A card-based layout for content organization

## Adding New Templates

To add a new template:

1. Create a new HTML file in the `app/templates` directory
2. Extend the base template: `{% extends "base.html" %}`
3. Define the content block: `{% block content %}...{% endblock %}`
4. Add a new route in `main.py` to render the template

## Customizing Templates

You can customize the templates by:

1. Modifying the CSS in `base.html`
2. Changing the layout structure
3. Adding new blocks for more customization points
4. Including additional static assets (JavaScript, images)

## Best Practices

When working with templates:

1. Keep logic in the Python code, not in templates
2. Use consistent naming for variables and blocks
3. Document the context variables expected by each template
4. Escape user-generated content to prevent XSS attacks

## Form Handling

The web interface includes forms for:

1. **Login**: Uses `username` and `password` fields
2. **Upload**: Uses a file input for uploading invoices

Forms are submitted using the standard HTML form mechanism with appropriate enctype:

```html
<form action="/web/process" method="post" enctype="multipart/form-data">
    <!-- Form fields -->
    <button type="submit">Submit</button>
</form>
```

## File Handling

The file upload form includes JavaScript for previewing files before submission:

```javascript
function previewFile() {
    const preview = document.getElementById('file-preview');
    const file = document.querySelector('input[type=file]').files[0];
    
    if (file) {
        // Show file details
        // If it's an image, show a preview
    }
}
```

## Security Considerations

The web interface implements several security measures:

1. **Authentication**: Protected routes require login
2. **CSRF Protection**: Forms use proper methods and authentication
3. **File Validation**: Uploaded files are validated by extension
4. **Error Handling**: Errors are caught and displayed appropriately

For a production application, you would want to add:
- CSRF tokens for forms
- Rate limiting for login attempts
- Secure cookie settings (HTTPS-only, SameSite)