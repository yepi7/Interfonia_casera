import numpy as np
import audioop
from scipy.io import wavfile
from scipy.signal import resample

# Configuración
input_ulaw = 'choose-sala.ulaw'
output_wav = 'choose-sala-decoded.wav'
target_rate = 8000  # Tasa de muestreo para G.711 µ-Law
original_rate = 48000  # Tasa de muestreo original

# Leer archivo G.711 µ-Law
with open(input_ulaw, 'rb') as f:
    ulaw_data = f.read()

# Decodificar audio de µ-Law a 16-bit PCM
def decode_audio(data):
    return audioop.ulaw2lin(data, 2)

# Decodificar audio
decoded_audio = decode_audio(ulaw_data)

# Convertir datos a un array numpy
decoded_audio_array = np.frombuffer(decoded_audio, dtype=np.int16)

# Cambiar la tasa de muestreo de 8 kHz a 48 kHz
num_samples = int(len(decoded_audio_array) * float(original_rate) / target_rate)
resampled_audio = resample(decoded_audio_array, num_samples)

# Guardar archivo WAV
wavfile.write(output_wav, original_rate, resampled_audio.astype(np.int16))

print(f'Archivo decodificado guardado como {output_wav}')
