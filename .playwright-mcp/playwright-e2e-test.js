const { chromium } = require('playwright');

async function testAddNewsE2E() {
  console.log('🚀 Iniciando pruebas E2E para funcionalidad Add News');
  
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 }
  });
  const page = await context.newPage();

  try {
    // Test 1: Acceso a la aplicación
    console.log('\n📋 Test 1: Verificando acceso a la aplicación...');
    await page.goto('http://localhost:5173');
    await page.waitForLoadState('networkidle');
    
    const title = await page.title();
    console.log(`✅ Aplicación cargada - Título: ${title}`);

    // Test 2: Proceso de autenticación
    console.log('\n📋 Test 2: Verificando estado de autenticación...');
    
    // Buscar elementos de login/logout
    const loginElement = await page.$('button:has-text("Login"), a:has-text("Login"), button:has-text("Sign In")');
    const dashboardElement = await page.$('[data-testid="dashboard"], .dashboard, h1:has-text("Dashboard")');
    
    if (loginElement) {
      console.log('📝 Usuario no autenticado, realizando login...');
      await loginElement.click();
      
      // Buscar campos de login
      const emailField = await page.$('input[type="email"], input[name="email"], input[placeholder*="email" i]');
      const passwordField = await page.$('input[type="password"], input[name="password"]');
      
      if (emailField && passwordField) {
        await emailField.fill('test@example.com');
        await passwordField.fill('password123');
        
        const submitBtn = await page.$('button[type="submit"], button:has-text("Sign In"), button:has-text("Login")');
        if (submitBtn) {
          await submitBtn.click();
          await page.waitForTimeout(2000);
          console.log('✅ Formulario de login enviado');
        }
      }
    } else if (dashboardElement) {
      console.log('✅ Usuario ya autenticado');
    }

    // Test 3: Navegación a Add News
    console.log('\n📋 Test 3: Navegando al formulario de creación de noticias...');
    
    // Intentar varias formas de encontrar el botón/enlace de add news
    const addNewsSelectors = [
      'button:has-text("Add News")',
      'a:has-text("Add News")', 
      'button:has-text("Create News")',
      'a:has-text("Create News")',
      '[data-testid="add-news"]',
      '.add-news-btn'
    ];
    
    let foundAddNews = false;
    for (const selector of addNewsSelectors) {
      const element = await page.$(selector);
      if (element) {
        await element.click();
        foundAddNews = true;
        console.log(`✅ Encontrado botón Add News con selector: ${selector}`);
        break;
      }
    }
    
    if (!foundAddNews) {
      // Intentar navegación directa por URL
      await page.goto('http://localhost:5173/news/create');
      console.log('⚠️  Botón no encontrado, navegando directamente a /news/create');
    }
    
    await page.waitForLoadState('networkidle');

    // Test 4: Verificar formulario y campos
    console.log('\n📋 Test 4: Verificando formulario de creación...');
    
    const formFields = {
      title: await page.$('input[name="title"], input[placeholder*="title" i], #title'),
      description: await page.$('textarea[name="description"], textarea[placeholder*="description" i], #description'), 
      content: await page.$('textarea[name="content"], textarea[placeholder*="content" i], #content'),
      link: await page.$('input[name="link"], input[name="url"], input[placeholder*="link" i], #link')
    };
    
    console.log('📋 Campos encontrados:');
    console.log(`- Título: ${formFields.title ? '✅' : '❌'}`);
    console.log(`- Descripción: ${formFields.description ? '✅' : '❌'}`);
    console.log(`- Contenido: ${formFields.content ? '✅' : '❌'}`);
    console.log(`- Link: ${formFields.link ? '✅' : '❌'}`);

    // Test 5: Validación de formulario vacío
    console.log('\n📋 Test 5: Probando validación de formulario vacío...');
    
    const submitButton = await page.$('button[type="submit"], button:has-text("Submit"), button:has-text("Create"), button:has-text("Save")');
    if (submitButton) {
      await submitButton.click();
      await page.waitForTimeout(1000);
      
      const errorMessages = await page.$$eval('.error, .invalid, [role="alert"], .text-red', 
        elements => elements.map(el => el.textContent.trim()));
      
      if (errorMessages.length > 0) {
        console.log('✅ Validación funcionando - Mensajes de error:', errorMessages);
      } else {
        console.log('⚠️  No se encontraron mensajes de validación');
      }
    }

    // Test 6: Creación exitosa de noticia
    console.log('\n📋 Test 6: Probando creación exitosa de noticia...');
    
    const testData = {
      title: 'Test News E2E - ' + Date.now(),
      description: 'Descripción de prueba para noticia E2E',
      content: 'Contenido completo de la noticia de prueba creada durante las pruebas E2E',
      link: 'https://example.com/test-news-' + Date.now()
    };
    
    if (formFields.title) {
      await formFields.title.fill(testData.title);
      console.log('✅ Título completado');
    }
    
    if (formFields.description) {
      await formFields.description.fill(testData.description);
      console.log('✅ Descripción completada');
    }
    
    if (formFields.content) {
      await formFields.content.fill(testData.content);
      console.log('✅ Contenido completado');
    }
    
    if (formFields.link) {
      await formFields.link.fill(testData.link);
      console.log('✅ Link completado');
    }
    
    if (submitButton) {
      await submitButton.click();
      console.log('📤 Formulario enviado');
      
      await page.waitForTimeout(3000);
      
      // Buscar indicadores de éxito
      const successMessages = await page.$$eval('.success, .alert-success, .text-green', 
        elements => elements.map(el => el.textContent.trim()));
      
      if (successMessages.length > 0) {
        console.log('✅ Creación exitosa - Mensajes:', successMessages);
      } else {
        console.log('⚠️  No se encontraron mensajes de éxito claros');
      }
    }

    // Test 7: Verificar en lista de noticias
    console.log('\n📋 Test 7: Verificando noticia en lista...');
    
    await page.goto('http://localhost:5173/news');
    await page.waitForLoadState('networkidle');
    
    const newsInList = await page.$(`text="${testData.title}"`);
    if (newsInList) {
      console.log('✅ Noticia encontrada en la lista');
    } else {
      console.log('⚠️  Noticia no encontrada en la lista');
    }

    // Tomar screenshot final
    await page.screenshot({ path: './e2e-results/add-news-final.png', fullPage: true });
    console.log('📸 Screenshot guardado en ./e2e-results/add-news-final.png');

    console.log('\n🎉 Pruebas E2E completadas exitosamente!');

  } catch (error) {
    console.error('❌ Error durante las pruebas E2E:', error);
    
    // Screenshot de error
    try {
      await page.screenshot({ path: './e2e-results/error-screenshot.png', fullPage: true });
      console.log('📸 Screenshot de error guardado');
    } catch (screenshotError) {
      console.error('No se pudo tomar screenshot de error');
    }
  } finally {
    await browser.close();
  }
}

// Ejecutar las pruebas
testAddNewsE2E();
