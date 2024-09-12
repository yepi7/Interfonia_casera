import socket
import struct
import numpy as np
import audioop
from scipy.io import wavfile

# Configuración
MCAST_GROUP = '239.255.0.1'
MCAST_PORT = 5004
CHUNK_SIZE = 160  # Tamaño de un bloque de audio en bytes

# Crear un socket UDP para la recepción
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))

# Unirse al grupo multicast
mreq = struct.pack('4sl', socket.inet_aton(MCAST_GROUP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

def decode_audio(data):
    # Decodifica el audio de G.711 µ-Law a PCM
    return audioop.ulaw2lin(data, 2)

decoded_audio = []

while True:
    data, _ = sock.recvfrom(CHUNK_SIZE + 12)  # 12 bytes para el encabezado RTP
    rtp_header = data[:12]  # Extrae el encabezado RTP
    audio_chunk = data[12:]  # Extrae los datos de audio
    decoded_chunk = decode_audio(audio_chunk)
    decoded_audio.append(decoded_chunk)

    # Opcional: Puedes agregar una condición para parar la recepción después de cierto tiempo o número de paquetes

# Guardar el audio decodificado en un archivo WAV
decoded_audio_bytes = b''.join(decoded_audio)
decoded_audio_array = np.frombuffer(decoded_audio_bytes, dtype=np.int16)
wavfile.write('received_audio.wav', 8000, decoded_audio_array)

print('Archivo de audio recibido y guardado como received_audio.wav')
