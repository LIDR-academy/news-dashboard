const { chromium } = require('playwright');

async function simpleE2ETest() {
  console.log('🚀 Ejecutando pruebas E2E simplificadas para Add News\n');
  
  const browser = await chromium.launch({ headless: false, slowMo: 500 });
  const context = await browser.newContext({ viewport: { width: 1280, height: 720 } });
  const page = await context.newPage();

  try {
    // Test 1: Acceso a la aplicación
    console.log('📋 Test 1: Accediendo a la aplicación...');
    await page.goto('http://localhost:5173');
    await page.waitForLoadState('networkidle');
    
    const title = await page.title();
    const url = page.url();
    console.log(`✅ Aplicación cargada - Título: ${title}, URL: ${url}`);
    await page.screenshot({ path: './e2e-results/step1-app-loaded.png', fullPage: true });

    // Test 2: Manejo de autenticación
    console.log('\n📋 Test 2: Verificando autenticación...');
    
    // Buscar elementos de login
    const loginButton = await page.locator('button:has-text("Login"), a:has-text("Login"), button:has-text("Sign In")').first();
    const isLoginVisible = await loginButton.isVisible().catch(() => false);
    
    if (isLoginVisible) {
      console.log('📝 Realizando login...');
      await loginButton.click();
      await page.waitForTimeout(1000);
      
      // Buscar campos de email y password
      const emailField = await page.locator('input[type="email"], input[name="email"], input[placeholder*="email" i]').first();
      const passwordField = await page.locator('input[type="password"], input[name="password"]').first();
      
      if (await emailField.isVisible() && await passwordField.isVisible()) {
        await emailField.fill('test@example.com');
        await passwordField.fill('password123');
        
        const submitBtn = await page.locator('button[type="submit"], button:has-text("Sign In"), button:has-text("Login")').first();
        if (await submitBtn.isVisible()) {
          await submitBtn.click();
          await page.waitForTimeout(3000);
          console.log('✅ Login enviado');
        }
      }
    } else {
      console.log('ℹ️  No se encontró login visible, posiblemente ya autenticado');
    }
    
    await page.screenshot({ path: './e2e-results/step2-after-auth.png', fullPage: true });

    // Test 3: Buscar navegación a Add News
    console.log('\n📋 Test 3: Buscando navegación a Add News...');
    
    // Listar elementos clickables con texto relevante
    const allButtons = await page.locator('button, a').all();
    const buttonTexts = [];
    
    for (let i = 0; i < Math.min(allButtons.length, 30); i++) {
      try {
        const text = await allButtons[i].textContent();
        const isVisible = await allButtons[i].isVisible();
        if (text && text.trim() && isVisible) {
          buttonTexts.push(text.trim());
        }
      } catch (e) {
        // Ignorar elementos que no se pueden leer
      }
    }
    
    console.log('🔍 Elementos clickables encontrados:', buttonTexts);
    
    // Buscar elementos relacionados con news
    const newsRelated = buttonTexts.filter(text => {
      const lowerText = text.toLowerCase();
      return lowerText.includes('news') || lowerText.includes('create') || 
             lowerText.includes('add') || lowerText.includes('new') ||
             lowerText.includes('noticia') || lowerText.includes('crear');
    });
    
    console.log('🔍 Elementos relacionados con news:', newsRelated);
    
    // Intentar encontrar botón de Add News
    const addNewsSelectors = [
      'button:has-text("Add News")',
      'a:has-text("Add News")',
      'button:has-text("Create News")', 
      'a:has-text("Create News")',
      'button:has-text("New")',
      'a:has-text("New")',
      '[data-testid*="add"], [data-testid*="create"], [data-testid*="news"]'
    ];
    
    let navigationFound = false;
    for (const selector of addNewsSelectors) {
      const element = page.locator(selector).first();
      const isVisible = await element.isVisible().catch(() => false);
      if (isVisible) {
        console.log(`✅ Encontrado elemento de navegación: ${selector}`);
        await element.click();
        navigationFound = true;
        await page.waitForTimeout(2000);
        break;
      }
    }
    
    if (!navigationFound) {
      console.log('⚠️  Navegación no encontrada, probando URLs directas...');
      const urls = [
        'http://localhost:5173/news/create',
        'http://localhost:5173/news/new',
        'http://localhost:5173/create-news',
        'http://localhost:5173/dashboard/news/create'
      ];
      
      for (const url of urls) {
        await page.goto(url);
        await page.waitForTimeout(2000);
        const currentUrl = page.url();
        console.log(`🔗 Probando: ${url} → ${currentUrl}`);
        
        if (!currentUrl.includes('404') && !currentUrl.includes('not-found')) {
          console.log(`✅ URL accesible: ${url}`);
          break;
        }
      }
    }
    
    await page.screenshot({ path: './e2e-results/step3-navigation.png', fullPage: true });

    // Test 4: Análisis del formulario
    console.log('\n📋 Test 4: Analizando formulario de creación...');
    
    // Buscar todos los inputs y textareas visibles
    const inputs = await page.locator('input').all();
    const textareas = await page.locator('textarea').all();
    
    console.log('🔍 Campos encontrados:');
    
    const foundFields = {};
    
    // Analizar inputs
    for (let i = 0; i < inputs.length; i++) {
      try {
        const input = inputs[i];
        const isVisible = await input.isVisible();
        if (isVisible) {
          const name = await input.getAttribute('name') || '';
          const placeholder = await input.getAttribute('placeholder') || '';
          const type = await input.getAttribute('type') || '';
          const id = await input.getAttribute('id') || '';
          
          console.log(`   Input[${i}]: name="${name}" placeholder="${placeholder}" type="${type}" id="${id}"`);
          
          // Identificar campos por nombre o placeholder
          const fieldText = (name + ' ' + placeholder + ' ' + id).toLowerCase();
          if (fieldText.includes('title') || fieldText.includes('titulo')) {
            foundFields.title = input;
          } else if (fieldText.includes('link') || fieldText.includes('url') || fieldText.includes('enlace')) {
            foundFields.link = input;
          }
        }
      } catch (e) {
        // Ignorar errores
      }
    }
    
    // Analizar textareas
    for (let i = 0; i < textareas.length; i++) {
      try {
        const textarea = textareas[i];
        const isVisible = await textarea.isVisible();
        if (isVisible) {
          const name = await textarea.getAttribute('name') || '';
          const placeholder = await textarea.getAttribute('placeholder') || '';
          const id = await textarea.getAttribute('id') || '';
          
          console.log(`   Textarea[${i}]: name="${name}" placeholder="${placeholder}" id="${id}"`);
          
          const fieldText = (name + ' ' + placeholder + ' ' + id).toLowerCase();
          if (fieldText.includes('description') || fieldText.includes('descripcion')) {
            foundFields.description = textarea;
          } else if (fieldText.includes('content') || fieldText.includes('contenido') || fieldText.includes('body')) {
            foundFields.content = textarea;
          }
        }
      } catch (e) {
        // Ignorar errores
      }
    }
    
    console.log(`\n📊 Resumen de campos identificados:`);
    console.log(`   - Título: ${foundFields.title ? '✅' : '❌'}`);
    console.log(`   - Descripción: ${foundFields.description ? '✅' : '❌'}`);
    console.log(`   - Contenido: ${foundFields.content ? '✅' : '❌'}`);
    console.log(`   - Link: ${foundFields.link ? '✅' : '❌'}`);

    // Test 5: Intentar llenar formulario
    if (Object.keys(foundFields).length > 0) {
      console.log('\n📋 Test 5: Llenando formulario...');
      
      const testData = {
        title: 'E2E Test News ' + Date.now(),
        description: 'Descripción de prueba para E2E testing',
        content: 'Contenido completo de la noticia de prueba E2E',
        link: 'https://example.com/e2e-test-' + Date.now()
      };
      
      for (const [fieldName, element] of Object.entries(foundFields)) {
        if (testData[fieldName]) {
          try {
            await element.fill(testData[fieldName]);
            console.log(`✅ Campo ${fieldName} completado`);
          } catch (e) {
            console.log(`❌ Error llenando ${fieldName}:`, e.message);
          }
        }
      }
      
      await page.screenshot({ path: './e2e-results/step4-form-filled.png', fullPage: true });
      
      // Buscar botón de submit
      const submitButtons = await page.locator('button[type="submit"], button:has-text("Submit"), button:has-text("Create"), button:has-text("Save"), button:has-text("Enviar"), button:has-text("Crear")').all();
      
      let submitFound = false;
      for (const btn of submitButtons) {
        const isVisible = await btn.isVisible();
        if (isVisible) {
          console.log('✅ Botón submit encontrado, enviando formulario...');
          await btn.click();
          submitFound = true;
          await page.waitForTimeout(5000);
          break;
        }
      }
      
      if (!submitFound) {
        console.log('❌ No se encontró botón de submit');
      }
      
      await page.screenshot({ path: './e2e-results/step5-after-submit.png', fullPage: true });
      
      // Buscar mensajes de respuesta
      const successElements = await page.locator('.success, .alert-success, [role="status"], .notification').all();
      const errorElements = await page.locator('.error, .alert-error, .alert-danger').all();
      
      console.log(`\n📊 Elementos de respuesta encontrados:`);
      console.log(`   - Mensajes de éxito: ${successElements.length}`);
      console.log(`   - Mensajes de error: ${errorElements.length}`);
      
      for (const element of [...successElements, ...errorElements]) {
        try {
          const text = await element.textContent();
          if (text && text.trim()) {
            console.log(`   📝 Mensaje: "${text.trim()}"`);
          }
        } catch (e) {
          // Ignorar errores
        }
      }
      
    } else {
      console.log('\n❌ Test 5: No se encontraron campos de formulario para llenar');
    }

    // Test 6: Verificar en lista de noticias
    console.log('\n📋 Test 6: Verificando lista de noticias...');
    await page.goto('http://localhost:5173/news');
    await page.waitForTimeout(2000);
    await page.screenshot({ path: './e2e-results/step6-news-list.png', fullPage: true });
    
    const newsItems = await page.locator('.news-item, .news-card, [data-testid*="news"]').count();
    console.log(`📊 Elementos de noticias encontrados en la lista: ${newsItems}`);

    console.log('\n🎉 Pruebas E2E simplificadas completadas!');
    console.log('📁 Revisa los screenshots en ./e2e-results/');

  } catch (error) {
    console.error('❌ Error durante las pruebas:', error);
    await page.screenshot({ path: './e2e-results/error-final.png', fullPage: true });
  } finally {
    await context.close();
    await browser.close();
  }
}

// Ejecutar pruebas
simpleE2ETest();
