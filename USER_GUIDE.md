# Adhoc Testing Agent User Guide

## Welcome

Welcome to the Adhoc Testing Agent! This guide will help you get started with generating and executing automated test scripts from natural language requirements.

## Getting Started

### Account Setup

1. **Register an Account**
   - Visit the application homepage
   - Click "Register" in the navigation
   - Fill in your details and select your role:
     - **Developer**: Can generate and execute tests
     - **QA Engineer**: Can view test history and rerun tests
     - **Admin**: Full system access including user management

2. **Login**
   - Use your credentials to log in
   - You'll be redirected to the home page

## Understanding Roles and Permissions

| Role | Generate Tests | Generate Code | View History | Rerun Tests | User Management |
|------|---------------|---------------|--------------|-------------|------------------|
| Developer | ✅ | ✅ | ✅ | ✅ | ❌ |
| QA Engineer | ❌ | ❌ | ✅ | ✅ | ❌ |
| Admin | ✅ | ✅ | ✅ | ✅ | ✅ |

## Generating Tests

### Basic Test Generation

1. **Navigate to Generate Page**
   - Click "Generate Test" in the navigation menu

2. **Select Browser**
   - Choose your preferred browser:
     - **Chrome/Chromium**: Most compatible, default choice
     - **Firefox**: Alternative browser testing
     - **Safari/WebKit**: macOS/iOS testing

3. **Choose a Predefined Requirement**
   - Use the dropdown to select common test scenarios
   - Or write your own custom requirement

4. **Write Your Requirement**
   - Describe what you want to test in plain English
   - Be specific about actions and expected outcomes
   - Examples:
     - "Test login functionality on SauceDemo website with valid credentials"
     - "Verify that search results appear when searching for 'laptop' on Amazon"
     - "Test adding an item to cart and proceeding to checkout"

5. **Generate and Execute**
   - Click "Generate & Execute Test"
   - Wait for the process to complete (may take 30-60 seconds)

### Code Generation

1. **Navigate to Generate Code Page**
   - Click "Generate Code" in the navigation menu

2. **Select Browser**
   - Choose your preferred browser for testing the generated code:
     - **Chrome/Chromium**: Most compatible, default choice
     - **Firefox**: Alternative browser testing
     - **Safari/WebKit**: macOS/iOS testing

3. **Write Your Code Requirement**
   - Describe the application feature you want to build in natural language
   - Be specific about functionality, UI elements, and expected behavior
   - Examples:
     - "Create a user profile page with edit functionality, including form validation and image upload"
     - "Build a blog post listing page with search, filtering, and pagination"
     - "Implement a shopping cart with add/remove items, quantity updates, and checkout"

4. **Upload Project ZIP (Optional but Recommended)**
   - Upload a ZIP file containing your existing project structure
   - This helps the AI understand your current codebase patterns, imports, and architecture
   - Include app.py, routes.py, models.py, and template files for best results

5. **Generate Code**
   - Click "Generate Code"
   - The system will analyze your project (if uploaded) and generate complete code
   - Wait for the process to complete (may take 1-2 minutes)

6. **Review Generated Code**
   - View the generated routes, templates, CSS, and JavaScript
   - See integration instructions with line numbers for adding to your project
   - Review the generated test script that validates the new functionality

### Understanding Test Results

After execution, you'll see several sections:

#### Generated Script
- The complete Playwright test script in Python
- Includes browser automation code
- Embedded statistics collection

#### Execution Result
- Pass/fail status
- Any error messages or output
- Browser behavior observations

#### Analysis (if applicable)
- Debugging information if the test failed
- Suggestions for script improvements

#### Test Statistics
- **Execution Time**: Total test duration
- **Assertions**: Number of passed/failed checks
- **Step Coverage**: Test steps completed
- **Performance**: Page load times and action speeds
- **Accessibility**: Detected accessibility issues
- **Locator Stability**: Element finding reliability

## Managing Test History

### Viewing Test History

1. **Access History Page**
   - Click "Test History" in the navigation

2. **Browse Tests**
   - View all your previous test executions
   - See requirement, timestamp, and result summary

3. **Search Tests**
   - Use the search box to find specific tests
   - Search by requirement text, script content, or results

4. **Pagination**
   - Navigate through multiple pages of results
   - 10 tests displayed per page

### Re-running Tests

1. **Find Test to Rerun**
   - Locate the test in history
   - Click the "Rerun" button

2. **Automatic Re-execution**
   - The system will regenerate and execute the test
   - New results will appear in history

### Downloading Test Scripts

1. **Download Option**
   - Click "Download" next to any test in history
   - Saves the script as a `.py` file

2. **Local Execution**
   - Run downloaded scripts locally with Python
   - Requires Playwright installation

## Best Practices

### Writing Effective Requirements

#### Be Specific
❌ "Test the website"
✅ "Test login functionality on SauceDemo with username 'standard_user' and password 'secret_sauce'"

#### Include Expected Outcomes
❌ "Click the login button"
✅ "Click the login button and verify user is redirected to the products page"

#### Use Action-Oriented Language
- "Navigate to..."
- "Enter text..."
- "Click button..."
- "Verify that..."

#### Test Complete User Journeys
- Login → Search → Add to Cart → Checkout
- Registration → Email Verification → Login
- Form Submission → Validation → Success Message

### Browser Selection Guidelines

| Browser | When to Use | Notes |
|---------|-------------|-------|
| Chrome/Chromium | Most websites, general testing | Fastest, most compatible |
| Firefox | Cross-browser validation | Good for compatibility testing |
| Safari/WebKit | macOS/iOS testing | Limited Windows support |

### Performance Considerations

- **Rate Limits**: 10 test generations per minute for developers
- **Execution Time**: Tests typically take 5-30 seconds
- **Timeout**: Maximum 5 minutes per test execution
- **Concurrent Users**: System handles multiple users simultaneously

## Troubleshooting

### Common Issues

#### Test Generation Fails
**Problem**: Script generation returns an error
**Solutions**:
- Check your requirement is clear and specific
- Ensure internet connection for AI API
- Try rephrasing your requirement
- Contact admin if issue persists

#### Test Execution Fails
**Problem**: Script runs but test fails
**Solutions**:
- Review the analysis section for debugging info
- Check if the target website has changed
- Verify your requirement matches actual site behavior
- Try a different browser

#### Browser Launch Issues
**Problem**: Browser doesn't open or crashes
**Solutions**:
- Ensure Playwright browsers are installed
- Check system has sufficient resources
- Try a different browser
- Restart the application

#### Slow Performance
**Problem**: Tests take longer than expected
**Solutions**:
- Check internet connection
- Verify target website isn't slow
- Try during off-peak hours
- Contact admin for system issues

### Error Messages

#### "Access denied"
- You don't have permission for this action
- Check your user role with an admin

#### "Rate limit exceeded"
- You've made too many requests
- Wait a few minutes before trying again

#### "Invalid requirement"
- Your requirement doesn't meet validation rules
- Make it more specific (10-1000 characters)
- Use allowed characters only

#### "Execution timed out"
- Test took too long to complete
- Simplify your requirement
- Check target website responsiveness

## Advanced Features

### Custom Test Scenarios

#### E-commerce Testing
```
Test complete purchase flow:
1. Login with valid credentials
2. Search for "wireless headphones"
3. Add first result to cart
4. Proceed to checkout
5. Enter shipping information
6. Complete payment with test card
7. Verify order confirmation
```

#### Form Validation Testing
```
Test user registration form:
1. Navigate to registration page
2. Try submitting empty form (verify errors)
3. Enter invalid email (verify error)
4. Enter weak password (verify error)
5. Enter valid data (verify success)
6. Try registering with existing email (verify error)
```

#### API-Driven Testing
```
Test search functionality:
1. Enter search term in search box
2. Click search button
3. Wait for results to load
4. Verify results contain search term
5. Check result count is greater than 0
6. Verify each result has title and price
```

### Statistics Interpretation

#### Performance Metrics
- **Page Load Time**: < 3 seconds is good
- **Action Time**: < 1 second per action is ideal
- **Total Execution**: Varies by test complexity

#### Assertion Results
- **High Pass Rate**: > 80% indicates good test design
- **Failed Assertions**: Review error messages for issues
- **Step Coverage**: 100% completion is ideal

#### Accessibility Score
- **0 violations**: Perfect accessibility
- **1-5 violations**: Minor issues, review warnings
- **>5 violations**: Significant accessibility problems

## Security and Privacy

### Data Handling
- All test data is stored securely
- Passwords are hashed and never displayed
- Test scripts may contain sensitive information
- Delete old tests if they contain private data

### Best Practices
- Don't include real passwords in test requirements
- Use test accounts for authentication testing
- Avoid testing on production systems without permission
- Be aware that browser automation may be detectable

## Getting Help

### Documentation
- **README.md**: Installation and setup
- **API_DOCUMENTATION.md**: Technical API details
- **ARCHITECTURE.md**: System design overview
- **DEPLOYMENT_GUIDE.md**: Production deployment

### Support Channels
1. **In-App Help**: Check error messages and analysis sections
2. **Admin Assistance**: Contact your system administrator
3. **GitHub Issues**: Report bugs or request features
4. **Community Forum**: Discuss with other users

### Contact Information
- **Technical Support**: [support email]
- **Documentation**: [docs URL]
- **Issue Tracker**: [GitHub URL]

## Frequently Asked Questions

### General Questions

**Q: What is the Adhoc Testing Agent?**
A: A web-based platform that converts natural language descriptions into automated test scripts using AI.

**Q: What browsers are supported?**
A: Chrome/Chromium, Firefox, and Safari/WebKit.

**Q: How long do tests take to run?**
A: Typically 5-30 seconds, depending on complexity.

**Q: Can I run tests locally?**
A: Yes, download scripts and run them with Python and Playwright.

### Technical Questions

**Q: What's the difference between roles?**
A: Developers create tests, QA engineers review and rerun, admins manage users.

**Q: Are there rate limits?**
A: Yes, 10 generations per minute for developers, 5 reruns per minute for QA.

**Q: Can I test mobile websites?**
A: The system uses desktop browsers, but you can test responsive design.

**Q: How are test statistics calculated?**
A: Through embedded code in generated scripts that tracks timing, assertions, and errors.

### Troubleshooting

**Q: My test keeps failing**
A: Check the analysis section, verify website hasn't changed, try different wording.

**Q: Browser doesn't launch**
A: Ensure Playwright is installed, check system resources, try different browser.

**Q: Getting timeout errors**
A: Simplify your test, check internet connection, try during off-peak hours.

---

Thank you for using the Adhoc Testing Agent! We hope this guide helps you create effective automated tests efficiently.

**Version**: 1.0.0
**Last Updated**: 2025
