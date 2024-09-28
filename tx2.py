import socket
import struct
import pyaudio
import audioop

# Configuración
MCAST_GROUP = '239.255.0.1'
MCAST_PORT = 5004
CHUNK_SIZE = 1024  # Tamaño del bloque de audio en bytes
RATE = 8000  # Tasa de muestreo para G.711 µ-Law
SSRC = 12345678  # Identificador SSRC
SEQ_NUM = 0  # Número de secuencia inicial

# Configurar el micrófono con PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,  # Formato de 16 bits
                channels=1,  # Audio mono
                rate=RATE,  # Tasa de muestreo
                input=True,  # Captura de entrada (micrófono)
                frames_per_buffer=CHUNK_SIZE)

# Crear un socket UDP para la transmisión
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)

def create_rtp_header(sequence_number, timestamp, ssrc):
    version = 2
    padding = 0
    extension = 0
    csrc_count = 0
    marker = 0
    payload_type = 0  # Payload Type para G.711 µ-Law

    first_byte = (version << 6) | (padding << 5) | (extension << 4) | csrc_count
    second_byte = (marker << 7) | payload_type

    return struct.pack('!BBHII', first_byte, second_byte, sequence_number, timestamp, ssrc)

timestamp = 0  # Inicializar timestamp

try:
    print("Transmisión de audio en tiempo real iniciada. Presiona Ctrl+C para detener.")
    while True:
        # Capturar audio del micrófono
        audio_data = stream.read(CHUNK_SIZE)

        # Convertir audio de 16-bit PCM a µ-Law
        encoded_audio = audioop.lin2ulaw(audio_data, 2)

        # Crear encabezado RTP
        rtp_header = create_rtp_header(SEQ_NUM, timestamp, SSRC)

        # Enviar paquete RTP
        sock.sendto(rtp_header + encoded_audio, (MCAST_GROUP, MCAST_PORT))

        # Incrementar número de secuencia y timestamp
        SEQ_NUM += 1
        timestamp += CHUNK_SIZE  # Ajuste de timestamp basado en el tamaño del bloque

except KeyboardInterrupt:
    print("Transmisión detenida.")

finally:
    # Cerrar el stream y el socket
    stream.stop_stream()
    stream.close()
    p.terminate()
    sock.close()
