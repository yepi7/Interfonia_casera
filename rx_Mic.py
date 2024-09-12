import socket
import struct
import numpy as np
import audioop
from scipy.io import wavfile

# Configuración
MCAST_GROUP = '239.255.0.1'
MCAST_PORT = 5004
CHUNK_SIZE = 160  # Tamaño del bloque de audio en bytes (160 bytes ≈ 20 ms para 8000 Hz)
RATE = 8000  # Tasa de muestreo para G.711 µ-Law

# Crear un socket UDP para la recepción
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))

# Unirse al grupo multicast
mreq = struct.pack('4sl', socket.inet_aton(MCAST_GROUP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Inicializar lista para almacenar datos de audio
decoded_audio = []

print("Recepción de audio en curso. Presiona Ctrl+C para detener.")

try:
    while True:
        data, _ = sock.recvfrom(CHUNK_SIZE + 12)  # 12 bytes para el encabezado RTP
        rtp_header = data[:12]  # Extraer el encabezado RTP
        audio_chunk = data[12:]  # Extraer los datos de audio
        decoded_chunk = audioop.ulaw2lin(audio_chunk, 2)
        decoded_audio.append(decoded_chunk)

except KeyboardInterrupt:
    print("Recepción detenida.")

finally:
    # Unir y guardar el audio decodificado en un archivo WAV
    decoded_audio_bytes = b''.join(decoded_audio)
    decoded_audio_array = np.frombuffer(decoded_audio_bytes, dtype=np.int16)
    wavfile.write('received_audio.wav', RATE, decoded_audio_array)
    sock.close()
