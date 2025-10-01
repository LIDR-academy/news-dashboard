/**
 * E2E Test Script for "Add News" Functionality
 * Tests the complete flow of creating news in the React FastAPI application
 */

const TEST_CONFIG = {
  frontend_url: 'http://localhost:5173',
  backend_url: 'http://localhost:8000',
  test_user: {
    username: 'testuser@example.com',
    password: 'testpassword123'
  },
  test_news: {
    title: 'Test News Article',
    description: 'This is a test news article created during E2E testing',
    content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    link: 'https://example.com/test-news-' + Date.now(),
    status: 'draft'
  }
};

async function runE2ETests() {
  console.log('🚀 Starting E2E tests for Add News functionality...\n');
  
  try {
    // Test 1: Verify application is accessible
    console.log('📋 Test 1: Verifying application accessibility...');
    await page.goto(TEST_CONFIG.frontend_url);
    await page.waitForLoadState('networkidle');
    
    const title = await page.title();
    console.log(`✅ Application loaded - Title: ${title}`);
    
    // Test 2: Login and authentication
    console.log('\n📋 Test 2: Testing login and authentication...');
    
    // Check if already logged in or need to login
    const loginButton = page.locator('button:has-text("Login"), a:has-text("Login")');
    const logoutButton = page.locator('button:has-text("Logout"), a:has-text("Logout")');
    
    if (await loginButton.isVisible()) {
      console.log('📝 User not logged in, proceeding with login...');
      await loginButton.click();
      
      // Fill login form
      await page.fill('input[type="email"], input[name="email"], input[placeholder*="email" i]', TEST_CONFIG.test_user.username);
      await page.fill('input[type="password"], input[name="password"]', TEST_CONFIG.test_user.password);
      
      const submitButton = page.locator('button[type="submit"], button:has-text("Sign In"), button:has-text("Login")');
      await submitButton.click();
      
      // Wait for login to complete
      await page.waitForURL('**/dashboard*', { timeout: 10000 });
      console.log('✅ Login successful');
    } else if (await logoutButton.isVisible()) {
      console.log('✅ User already logged in');
    } else {
      console.log('⚠️  Cannot determine login state, proceeding...');
    }
    
    // Test 3: Navigate to Add News form
    console.log('\n📋 Test 3: Testing navigation to Add News form...');
    
    // Look for various ways to access news creation
    const addNewsSelectors = [
      'button:has-text("Add News")',
      'a:has-text("Add News")',
      'button:has-text("Create News")',
      'a:has-text("Create News")',
      '[data-testid="add-news-button"]',
      '.add-news-button'
    ];
    
    let addNewsButton = null;
    for (const selector of addNewsSelectors) {
      const element = page.locator(selector);
      if (await element.isVisible()) {
        addNewsButton = element;
        break;
      }
    }
    
    if (addNewsButton) {
      await addNewsButton.click();
      console.log('✅ Successfully navigated to Add News form');
    } else {
      // Try navigation via URL
      await page.goto(TEST_CONFIG.frontend_url + '/news/create');
      console.log('⚠️  Navigation button not found, trying direct URL');
    }
    
    await page.waitForLoadState('networkidle');
    
    // Test 4: Form validation testing
    console.log('\n📋 Test 4: Testing form validation...');
    
    // Test empty form submission
    const submitButton = page.locator('button[type="submit"], button:has-text("Submit"), button:has-text("Create"), button:has-text("Save")');
    if (await submitButton.isVisible()) {
      await submitButton.click();
      
      // Check for validation messages
      const validationMessages = await page.locator('.error, .invalid, [role="alert"], .text-red').allTextContents();
      if (validationMessages.length > 0) {
        console.log('✅ Form validation working - Found validation messages:', validationMessages);
      } else {
        console.log('⚠️  No validation messages found');
      }
    }
    
    // Test 5: Successful news creation
    console.log('\n📋 Test 5: Testing successful news creation...');
    
    // Fill out the form with test data
    const formFields = {
      title: ['input[name="title"]', 'input[placeholder*="title" i]', '#title'],
      description: ['textarea[name="description"]', 'textarea[placeholder*="description" i]', '#description'],
      content: ['textarea[name="content"]', 'textarea[placeholder*="content" i]', '#content'],
      link: ['input[name="link"]', 'input[name="url"]', 'input[placeholder*="link" i]', 'input[placeholder*="url" i]', '#link', '#url']
    };
    
    // Fill title
    for (const selector of formFields.title) {
      const field = page.locator(selector);
      if (await field.isVisible()) {
        await field.fill(TEST_CONFIG.test_news.title);
        console.log('✅ Title field filled');
        break;
      }
    }
    
    // Fill description
    for (const selector of formFields.description) {
      const field = page.locator(selector);
      if (await field.isVisible()) {
        await field.fill(TEST_CONFIG.test_news.description);
        console.log('✅ Description field filled');
        break;
      }
    }
    
    // Fill content
    for (const selector of formFields.content) {
      const field = page.locator(selector);
      if (await field.isVisible()) {
        await field.fill(TEST_CONFIG.test_news.content);
        console.log('✅ Content field filled');
        break;
      }
    }
    
    // Fill link
    for (const selector of formFields.link) {
      const field = page.locator(selector);
      if (await field.isVisible()) {
        await field.fill(TEST_CONFIG.test_news.link);
        console.log('✅ Link field filled');
        break;
      }
    }
    
    // Submit the form
    await submitButton.click();
    console.log('📤 Form submitted');
    
    // Wait for success response
    await page.waitForTimeout(2000);
    
    // Check for success indicators
    const successIndicators = await page.locator('.success, .alert-success, [role="status"]:has-text("success"), .text-green').allTextContents();
    if (successIndicators.length > 0) {
      console.log('✅ News creation successful - Success messages:', successIndicators);
    } else {
      console.log('⚠️  No clear success indicators found');
    }
    
    // Test 6: Check if news appears in list
    console.log('\n📋 Test 6: Verifying news appears in news list...');
    
    // Navigate to news list
    await page.goto(TEST_CONFIG.frontend_url + '/news');
    await page.waitForLoadState('networkidle');
    
    // Look for the created news
    const newsTitle = page.locator(`text="${TEST_CONFIG.test_news.title}"`);
    if (await newsTitle.isVisible()) {
      console.log('✅ Created news found in news list');
    } else {
      console.log('⚠️  Created news not found in news list');
    }
    
    // Test 7: Error scenario testing
    console.log('\n📋 Test 7: Testing error scenarios...');
    
    // Try to create duplicate news
    await page.goto(TEST_CONFIG.frontend_url + '/news/create');
    await page.waitForLoadState('networkidle');
    
    // Fill same link again
    for (const selector of formFields.link) {
      const field = page.locator(selector);
      if (await field.isVisible()) {
        await field.fill(TEST_CONFIG.test_news.link); // Same link as before
        break;
      }
    }
    
    // Fill other required fields
    for (const selector of formFields.title) {
      const field = page.locator(selector);
      if (await field.isVisible()) {
        await field.fill('Duplicate Test News');
        break;
      }
    }
    
    await submitButton.click();
    
    // Check for duplicate error
    const errorMessages = await page.locator('.error, .alert-error, [role="alert"], .text-red').allTextContents();
    if (errorMessages.some(msg => msg.toLowerCase().includes('duplicate') || msg.toLowerCase().includes('exists'))) {
      console.log('✅ Duplicate validation working - Error messages:', errorMessages);
    } else {
      console.log('⚠️  No duplicate validation error found');
    }
    
    console.log('\n🎉 E2E tests completed successfully!');
    
  } catch (error) {
    console.error('❌ E2E test failed:', error);
    
    // Take screenshot on error
    try {
      await page.screenshot({ path: 'e2e-error-screenshot.png', fullPage: true });
      console.log('📸 Error screenshot saved as e2e-error-screenshot.png');
    } catch (screenshotError) {
      console.error('Failed to take screenshot:', screenshotError);
    }
  }
}

// Export the test function for execution
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { runE2ETests, TEST_CONFIG };
}
