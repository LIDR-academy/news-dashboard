const { chromium } = require('playwright');

async function enhancedE2ETest() {
  console.log('🚀 Re-ejecutando pruebas E2E mejoradas para Add News');
  console.log('🔧 Configuración: Mayor detalle de debugging y captura de información\n');
  
  const browser = await chromium.launch({ 
    headless: false,
    slowMo: 1000 // Slow down para mejor observación
  });
  
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    recordVideo: {
      dir: './e2e-results/videos/',
      size: { width: 1280, height: 720 }
    }
  });
  
  const page = await context.newPage();

  try {
    // Test 1: Acceso inicial con más detalle
    console.log('📋 Test 1: Acceso detallado a la aplicación...');
    await page.goto('http://localhost:5173');
    await page.waitForLoadState('networkidle');
    
    const title = await page.title();
    const url = page.url();
    console.log(`✅ Aplicación cargada:`);
    console.log(`   - Título: ${title}`);
    console.log(`   - URL: ${url}`);
    
    // Capturar screenshot inicial
    await page.screenshot({ path: './e2e-results/01-initial-load.png', fullPage: true });

    // Test 2: Análisis de estado de autenticación más detallado
    console.log('\n📋 Test 2: Análisis detallado de autenticación...');
    
    // Buscar todos los elementos relacionados con auth
    const authElements = await page.$$eval('*', elements => {
      return elements.filter(el => {
        const text = (el.textContent || '').toLowerCase();
        const classes = (el.className || '').toLowerCase();
        const id = (el.id || '').toLowerCase();
        return text.includes('login') || text.includes('logout') || 
               text.includes('sign in') || text.includes('sign out') ||
               classes.includes('login') || classes.includes('auth') ||
               id.includes('login') || id.includes('auth');
      }).map(el => ({
        tag: el.tagName,
        text: (el.textContent || '').trim(),
        className: el.className || '',
        id: el.id || ''
      }));
    });
    
    console.log('🔍 Elementos de autenticación encontrados:', authElements);
    
    // Intentar login si es necesario
    const loginButton = await page.$('button:has-text("Login"), a:has-text("Login"), button:has-text("Sign In")');
    if (loginButton) {
      console.log('📝 Procediendo con login...');
      await loginButton.click();
      await page.waitForTimeout(2000);
      await page.screenshot({ path: './e2e-results/02-login-form.png', fullPage: true });
      
      // Buscar campos de login con más selectores
      const emailSelectors = [
        'input[type="email"]',
        'input[name="email"]', 
        'input[name="username"]',
        'input[placeholder*="email" i]',
        'input[placeholder*="user" i]',
        '#email', '#username', '#user'
      ];
      
      const passwordSelectors = [
        'input[type="password"]',
        'input[name="password"]',
        'input[placeholder*="password" i]',
        '#password', '#pass'
      ];
      
      let emailField = null;
      let passwordField = null;
      
      for (const selector of emailSelectors) {
        const field = await page.$(selector);
        if (field && await field.isVisible()) {
          emailField = field;
          console.log(`✅ Campo email encontrado: ${selector}`);
          break;
        }
      }
      
      for (const selector of passwordSelectors) {
        const field = await page.$(selector);
        if (field && await field.isVisible()) {
          passwordField = field;
          console.log(`✅ Campo password encontrado: ${selector}`);
          break;
        }
      }
      
      if (emailField && passwordField) {
        await emailField.fill('test@example.com');
        await passwordField.fill('password123');
        
        const submitButton = await page.$('button[type="submit"], button:has-text("Sign In"), button:has-text("Login")');
        if (submitButton) {
          await submitButton.click();
          await page.waitForTimeout(3000);
          console.log('✅ Login enviado, esperando respuesta...');
          
          await page.screenshot({ path: './e2e-results/03-after-login.png', fullPage: true });
        }
      }
    } else {
      console.log('ℹ️  No se encontró botón de login, posiblemente ya autenticado');
    }

    // Test 3: Análisis exhaustivo de navegación
    console.log('\n📋 Test 3: Búsqueda exhaustiva de navegación a Add News...');
    
    // Listar todos los elementos clicables
    const clickableElements = await page.$$eval('button, a, [role="button"], [onclick]', elements => {
      return elements.map(el => ({
        tag: el.tagName,
        text: (el.textContent || '').trim(),
        href: el.href || '',
        className: el.className || '',
        id: el.id || '',
        role: el.getAttribute('role') || ''
      })).filter(el => el.text && el.text.length > 0);
    });
    
    console.log('🔍 Elementos clicables encontrados:');
    clickableElements.forEach((el, i) => {
      if (i < 20) { // Mostrar solo los primeros 20
        console.log(`   ${i+1}. ${el.tag}: "${el.text}" (class: ${el.className})`);
      }
    });
    
    // Buscar elementos relacionados con news
    const newsElements = clickableElements.filter(el => {
      const text = el.text.toLowerCase();
      return text.includes('news') || text.includes('noticia') || 
             text.includes('create') || text.includes('add') ||
             text.includes('crear') || text.includes('agregar');
    });
    
    console.log('\n🔍 Elementos relacionados con news/crear:');
    newsElements.forEach(el => {
      console.log(`   - ${el.tag}: "${el.text}" (class: ${el.className})`);
    });
    
    // Intentar diferentes formas de navegar
    const navigationAttempts = [
      'button:has-text("Add News")',
      'a:has-text("Add News")',
      'button:has-text("Create News")',
      'a:has-text("Create News")',
      'button:has-text("New News")',
      'a:has-text("New News")',
      '[data-testid="add-news"]',
      '[data-testid="create-news"]',
      '.add-news', '.create-news',
      'button:has-text("+")',
      'a[href*="create"]',
      'a[href*="new"]'
    ];
    
    let navigationSuccess = false;
    for (const selector of navigationAttempts) {
      const element = await page.$(selector);
      if (element && await element.isVisible()) {
        console.log(`✅ Navegación encontrada con: ${selector}`);
        await element.click();
        navigationSuccess = true;
        await page.waitForTimeout(2000);
        break;
      }
    }
    
    if (!navigationSuccess) {
      console.log('⚠️  Navegación no encontrada, probando URLs directas...');
      const urls = [
        'http://localhost:5173/news/create',
        'http://localhost:5173/news/new',
        'http://localhost:5173/create-news',
        'http://localhost:5173/add-news'
      ];
      
      for (const url of urls) {
        try {
          await page.goto(url);
          await page.waitForTimeout(2000);
          const currentUrl = page.url();
          console.log(`🔗 Probando URL: ${url} → ${currentUrl}`);
          
          if (!currentUrl.includes('404') && !currentUrl.includes('not-found')) {
            console.log(`✅ URL funcionando: ${url}`);
            break;
          }
        } catch (error) {
          console.log(`❌ URL no accesible: ${url}`);
        }
      }
    }
    
    await page.screenshot({ path: './e2e-results/04-after-navigation.png', fullPage: true });

    // Test 4: Análisis exhaustivo del formulario
    console.log('\n📋 Test 4: Análisis exhaustivo del formulario...');
    
    // Listar todos los inputs y textareas
    const formElements = await page.$$eval('input, textarea, select', elements => {
      return elements.map(el => ({
        tag: el.tagName,
        type: el.type || '',
        name: el.name || '',
        id: el.id || '',
        className: el.className || '',
        placeholder: el.placeholder || '',
        required: el.required || false,
        visible: el.offsetParent !== null
      }));
    });
    
    console.log('🔍 Elementos de formulario encontrados:');
    formElements.forEach((el, i) => {
      console.log(`   ${i+1}. ${el.tag}[${el.type}] name="${el.name}" id="${el.id}" placeholder="${el.placeholder}" visible=${el.visible}`);
    });
    
    // Buscar formularios
    const forms = await page.$$eval('form', forms => {
      return forms.map(form => ({
        action: form.action || '',
        method: form.method || '',
        className: form.className || '',
        id: form.id || ''
      }));
    });
    
    console.log('🔍 Formularios encontrados:', forms);
    
    // Intentar llenar formulario con selectores más amplios
    const fieldMappings = {
      title: [
        'input[name="title"]', 'input[name="titulo"]',
        'input[placeholder*="title" i]', 'input[placeholder*="titulo" i]',
        '#title', '#titulo', '.title-input', '.titulo-input'
      ],
      description: [
        'textarea[name="description"]', 'textarea[name="descripcion"]',
        'input[name="description"]', 'input[name="descripcion"]',
        'textarea[placeholder*="description" i]', 'textarea[placeholder*="descripcion" i]',
        '#description', '#descripcion', '.description-input'
      ],
      content: [
        'textarea[name="content"]', 'textarea[name="contenido"]',
        'textarea[name="body"]', 'textarea[name="text"]',
        'textarea[placeholder*="content" i]', 'textarea[placeholder*="contenido" i]',
        '#content', '#contenido', '#body', '.content-input'
      ],
      link: [
        'input[name="link"]', 'input[name="url"]', 'input[name="enlace"]',
        'input[type="url"]',
        'input[placeholder*="link" i]', 'input[placeholder*="url" i]', 'input[placeholder*="enlace" i]',
        '#link', '#url', '#enlace', '.link-input', '.url-input'
      ]
    };
    
    const foundFields = {};
    for (const [fieldName, selectors] of Object.entries(fieldMappings)) {
      for (const selector of selectors) {
        const field = await page.$(selector);
        if (field && await field.isVisible()) {
          foundFields[fieldName] = selector;
          console.log(`✅ Campo ${fieldName} encontrado: ${selector}`);
          break;
        }
      }
      if (!foundFields[fieldName]) {
        console.log(`❌ Campo ${fieldName} NO encontrado`);
      }
    }
    
    // Test 5: Intentar crear noticia si hay formulario
    if (Object.keys(foundFields).length > 0) {
      console.log('\n📋 Test 5: Intentando crear noticia...');
      
      const testData = {
        title: 'E2E Test News ' + Date.now(),
        description: 'Descripción de prueba E2E mejorada',
        content: 'Contenido completo de prueba para noticia E2E con análisis detallado',
        link: 'https://example.com/e2e-test-' + Date.now()
      };
      
      for (const [field, data] of Object.entries(testData)) {
        if (foundFields[field]) {
          await page.fill(foundFields[field], data);
          console.log(`✅ Campo ${field} completado con: ${data}`);
        }
      }
      
      await page.screenshot({ path: './e2e-results/05-form-filled.png', fullPage: true });
      
      // Buscar botón de envío
      const submitSelectors = [
        'button[type="submit"]',
        'input[type="submit"]',
        'button:has-text("Submit")', 'button:has-text("Create")', 'button:has-text("Save")',
        'button:has-text("Enviar")', 'button:has-text("Crear")', 'button:has-text("Guardar")',
        '.submit-btn', '.create-btn', '.save-btn'
      ];
      
      let submitButton = null;
      for (const selector of submitSelectors) {
        const btn = await page.$(selector);
        if (btn && await btn.isVisible()) {
          submitButton = btn;
          console.log(`✅ Botón submit encontrado: ${selector}`);
          break;
        }
      }
      
      if (submitButton) {
        await submitButton.click();
        console.log('📤 Formulario enviado, esperando respuesta...');
        await page.waitForTimeout(5000);
        
        await page.screenshot({ path: './e2e-results/06-after-submit.png', fullPage: true });
        
        // Buscar mensajes de respuesta
        const messages = await page.$$eval('*', elements => {
          return elements.filter(el => {
            const text = (el.textContent || '').toLowerCase();
            const classes = (el.className || '').toLowerCase();
            return (text.includes('success') || text.includes('error') || 
                   text.includes('éxito') || text.includes('error') ||
                   classes.includes('success') || classes.includes('error') ||
                   classes.includes('alert') || classes.includes('notification')) &&
                   el.offsetParent !== null; // Solo elementos visibles
          }).map(el => ({
            text: (el.textContent || '').trim(),
            className: el.className || ''
          }));
        });
        
        console.log('🔍 Mensajes de respuesta encontrados:', messages);
      }
    } else {
      console.log('\n❌ Test 5: No se puede probar creación - formulario no accesible');
    }
    
    // Captura final del estado
    await page.screenshot({ path: './e2e-results/07-final-state.png', fullPage: true });
    
    console.log('\n🎉 Pruebas E2E mejoradas completadas!');
    console.log('📁 Revisa los screenshots en ./e2e-results/ para análisis visual');

  } catch (error) {
    console.error('❌ Error durante pruebas E2E mejoradas:', error);
    await page.screenshot({ path: './e2e-results/error-enhanced.png', fullPage: true });
  } finally {
    await context.close();
    await browser.close();
  }
}

// Ejecutar las pruebas mejoradas
enhancedE2ETest();
