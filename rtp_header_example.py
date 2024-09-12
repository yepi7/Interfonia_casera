import struct

def create_rtp_header(version, padding, extension, csrc_count, marker, payload_type, sequence_number, timestamp, ssrc):
    # RTP Header Fields
    version = (version & 0x03) << 6
    padding = (padding & 0x01) << 5
    extension = (extension & 0x01) << 4
    csrc_count = (csrc_count & 0x0F)
    
    first_byte = version | padding | extension | csrc_count
    second_byte = (marker << 7) | (payload_type & 0x7F)
    
    # Pack RTP header
    rtp_header = struct.pack(
        '!BBHII',  # Format string for RTP header
        first_byte,  # Version, Padding, Extension, CSRC Count
        second_byte,  # Marker, Payload Type
        sequence_number,  # Sequence Number
        timestamp,  # Timestamp
        ssrc  # SSRC
    )
    
    return rtp_header

# Example values
version = 2
padding = 0
extension = 0
csrc_count = 0
marker = 0
payload_type = 0  # For PCMU (G.711 µ-Law), use 0
sequence_number = 1234
timestamp = 5678
ssrc = 98765432

# Create RTP header
rtp_header = create_rtp_header(version, padding, extension, csrc_count, marker, payload_type, sequence_number, timestamp, ssrc)

print(f"RTP Header: {rtp_header.hex()}")
