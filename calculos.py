# calculos señal EMG
import os
import matplotlib
matplotlib.use('Agg')  # Backend sin interfaz gráfica para servidores como Render
import numpy as np
import matplotlib.pyplot as plt

def analizar_emg(muestras):
    emg = np.array(muestras, dtype=float)  # Convertir datos a arreglo NumPy

    # Parámetros estadísticos
    valor_rms = np.sqrt(np.mean(emg**2))
    promedio = np.mean(emg)
    desviacion = np.std(emg)
    maximo = np.max(emg)

    # FFT
    fft = np.fft.fft(emg)
    magnitud_fft = np.abs(fft)
    pico_fft = np.max(magnitud_fft)

    # Clasificación
    if desviacion > 15:
        estado = "Posible fatiga muscular"
    elif valor_rms > 30:
        estado = "Contracción fuerte"
    elif valor_rms > 15:
        estado = "Contracción moderada"
    else:
        estado = "Actividad baja"

    # Asegurar que la carpeta static exista en el servidor
    os.makedirs("static", exist_ok=True)

    # Gráfica EMG
    plt.figure(figsize=(8, 4))
    plt.plot(emg, '-ob')
    plt.title("Señal EMG")
    plt.xlabel("Muestras")
    plt.ylabel("Amplitud")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("static/emg.png")
    plt.close()

    # Gráfica FFT
    plt.figure(figsize=(8, 4))
    plt.stem(magnitud_fft)
    plt.title("FFT de la señal")
    plt.xlabel("Frecuencia")
    plt.ylabel("Magnitud")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("static/fft.png")
    plt.close()

    # Resultados
    return {
        "rms": float(round(valor_rms, 2)),
        "promedio": float(round(promedio, 2)),
        "maximo": float(round(maximo, 2)),
        "desviacion": float(round(desviacion, 2)),
        "pico_fft": float(round(pico_fft, 2)),
        "estado": estado
    }
