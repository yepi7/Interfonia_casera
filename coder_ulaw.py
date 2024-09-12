import numpy as np
import audioop
from scipy.io import wavfile
from scipy.signal import resample

# Configuración
input_wav = 'choose-sala.wav'
output_ulaw = 'choose-sala.ulaw'
target_rate = 8000  # Tasa de muestreo para G.711 µ-Law

# Leer el archivo WAV
rate, audio_data = wavfile.read(input_wav)

# Verificar si el audio es estéreo y convertir a mono si es necesario
if len(audio_data.shape) > 1:
    audio_data = audio_data[:, 0]

# Cambiar la tasa de muestreo de 48 kHz a 8 kHz
num_samples = int(len(audio_data) * float(target_rate) / rate)
resampled_audio = resample(audio_data, num_samples)

# Convertir audio de 16-bit PCM a µ-Law
def encode_audio(data):
    return audioop.lin2ulaw(data, 2)

# Codificar audio
encoded_audio = encode_audio(resampled_audio.astype(np.int16).tobytes())

# Guardar archivo G.711 µ-Law
with open(output_ulaw, 'wb') as f:
    f.write(encoded_audio)

print(f'Archivo codificado guardado como {output_ulaw}')
