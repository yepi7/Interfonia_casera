import socket
import struct
import pyaudio
import audioop

# Configuración
MCAST_GROUP = '239.255.0.1'
MCAST_PORT = 5004
CHUNK_SIZE = 1024  # Tamaño del bloque de audio en bytes
RATE = 8000  # Tasa de muestreo (8000 Hz)

# Crear un socket UDP para la recepción
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))

# Unirse al grupo multicast
mreq = struct.pack('4sl', socket.inet_aton(MCAST_GROUP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Configurar PyAudio para reproducir el audio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,  # Formato de 16 bits
                channels=1,  # Audio mono
                rate=RATE,  # Tasa de muestreo
                output=True)  # Salida (reproducir)

def decode_audio(data):
    # Decodificar el audio de G.711 µ-Law a PCM
    return audioop.ulaw2lin(data, 2)

try:
    print("Reproduciendo audio en tiempo real...")
    while True:
        # Recibir paquete RTP
        data, _ = sock.recvfrom(CHUNK_SIZE + 12)  # 12 bytes para el encabezado RTP
        audio_chunk = data[12:]  # Extraer los datos de audio
        decoded_chunk = decode_audio(audio_chunk)
        stream.write(decoded_chunk)  # Reproducir el audio decodificado

except KeyboardInterrupt:
    print("Recepción detenida.")

finally:
    # Cerrar el stream y el socket
    stream.stop_stream()
    stream.close()
    p.terminate()
    sock.close()
