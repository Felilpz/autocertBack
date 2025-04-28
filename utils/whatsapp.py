from playwright.sync_api import sync_playwright

def iniciar_whatsapp(numero_telefone, mensagem):
    with sync_playwright() as p:
        # Inicia o navegador Chromium
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Acessa o WhatsApp Web
        page.goto("https://web.whatsapp.com/")
        
        # Espera o QR Code carregar e aparecer
        print("Esperando pelo QR Code...")
        page.wait_for_selector('canvas[aria-label="Scan me!"]', timeout=120000)  # Timeout aumentado para 2 minutos
        
        # Aqui você pode capturar o QR Code ou qualquer outra lógica que deseja
        print("QR Code pronto para ser escaneado.")
        
        # Após escanear o QR Code, você pode enviar a mensagem para o número
        page.goto(f'https://web.whatsapp.com/send?phone={numero_telefone}&text={mensagem}')
        page.wait_for_timeout(5000)  # Aguardar alguns segundos para garantir que o envio é possível
        
        # Envia a mensagem
        page.locator('span[data-icon="send"]').click()
        
        print("Mensagem enviada!")
        
        # Fecha o navegador
        browser.close()
