import socket
import struct
import numpy as np
import pyaudio
import audioop

# Configuración
MCAST_GROUP = '239.255.0.1'
MCAST_PORT = 5004
CHUNK_SIZE = 160  # Tamaño del bloque de audio en bytes (160 bytes ≈ 20 ms para 8000 Hz)
RATE = 8000  # Tasa de muestreo para G.711 µ-Law
SSRC = 12345678  # Identificador SSRC
SEQ_NUM = 0  # Número de secuencia inicial

# Configuración de PyAudio
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK_SIZE
)

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

    return struct.pack(
        '!BBHII',  # Formato para el encabezado RTP
        first_byte,  # Versión, Padding, Extension, CSRC Count
        second_byte,  # Marker, Payload Type
        sequence_number,  # Número de secuencia
        timestamp,  # Timestamp
        ssrc  # SSRC
    )

timestamp = 0  # Inicializar timestamp

print("Transmisión de audio en curso. Presiona Ctrl+C para detener.")

try:
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
        timestamp += CHUNK_SIZE

except KeyboardInterrupt:
    print("Transmisión detenida.")

finally:
    # Cerrar el stream y el socket
    stream.stop_stream()
    stream.close()
    p.terminate()
    sock.close()
