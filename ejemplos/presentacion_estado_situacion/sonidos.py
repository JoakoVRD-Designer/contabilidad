# Sonidos propios (sintetizados, sin derechos de autor) para las transiciones de la presentación.
# entrada.wav: arpegio suave de 3 notas (portada) · pasar.wav: "whoosh" muy suave · logro.wav: campanita de 2 notas.
import array, math, random, wave, os

SR = 44100
DIR = os.path.dirname(os.path.abspath(__file__))
random.seed(7)


def guardar(nombre, x, pico):
    m = max(abs(v) for v in x)
    g = pico / m
    # fundido final de 40 ms para que no haga "clic"
    n = int(0.04 * SR)
    for i in range(n):
        x[-1 - i] *= i / n
    datos = array.array("h", [int(max(-1.0, min(1.0, v * g)) * 32767) for v in x])
    with wave.open(os.path.join(DIR, nombre), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(datos.tobytes())
    rms = math.sqrt(sum((v * g) ** 2 for v in x) / len(x))
    print(f"{nombre}: {len(x) / SR:.2f} s · pico {20 * math.log10(pico):.1f} dBFS · rms {20 * math.log10(rms):.1f} dBFS")


def nota(buf, t0, f, parciales, amp=1.0):
    """parciales: [(multiplo, amplitud, tau_segundos)]"""
    i0 = int(t0 * SR)
    for i in range(i0, len(buf)):
        t = (i - i0) / SR
        ataque = min(1.0, t / 0.004)
        v = 0.0
        for k, a, tau in parciales:
            v += a * math.exp(-t / tau) * math.sin(2 * math.pi * f * k * t)
        buf[i] += amp * ataque * v


# 1) Entrada: Do5-Mi5-Sol5, timbre tipo marimba suave
x = [0.0] * int(1.25 * SR)
marimba = [(1, 1.0, 0.30), (2, 0.16, 0.12), (4, 0.10, 0.05)]
for j, f in enumerate([523.25, 659.26, 783.99]):
    nota(x, 0.11 * j, f, marimba, amp=0.85 + 0.05 * j)
guardar("entrada.wav", x, 0.28)

# 2) Pasar: ruido filtrado con barrido de frecuencia (filtro de estado variable)
dur = 0.42
n = int(dur * SR)
x = [0.0] * n
low = band = 0.0
q = 1 / 0.9
for i in range(n):
    p = i / n
    fc = 300 * (3200 / 300) ** p if p < 0.6 else 3200 * (900 / 3200) ** ((p - 0.6) / 0.4)
    f = 2 * math.sin(math.pi * fc / SR)
    ruido = random.uniform(-1, 1)
    high = ruido - low - q * band
    band += f * high
    low += f * band
    env = math.sin(math.pi * min(1.0, p / 0.45) / 2) ** 2 if p < 0.45 else math.cos(math.pi * (p - 0.45) / 0.55 / 2) ** 2
    x[i] = band * env
guardar("pasar.wav", x, 0.20)

# 3) Logro: Mi5 -> La5, timbre de campanita
x = [0.0] * int(1.15 * SR)
campana = [(1, 1.0, 0.42), (2.76, 0.22, 0.11), (5.4, 0.07, 0.05)]
nota(x, 0.0, 659.26, campana, amp=0.9)
nota(x, 0.12, 880.0, campana, amp=1.0)
guardar("logro.wav", x, 0.26)
