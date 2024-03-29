from __future__ import annotations

import socket
import struct
import asyncio


class RCON:
    SERVER_DATA_AUTH_ID = 3
    SERVER_DATA_EXEC_COMMAND_ID = 2
    SERVER_DATA_RESPONSE_VALUE = 0
    EMPTY_BYTE_STRING = b"\x00\x00"

    def __init__(self) -> None:
        self.__socket: socket.socket | None = None

    async def __aenter__(self) -> RCON:
        await self.connect_to_rcon()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close_connection()

    async def connect_to_rcon(self, server_ip: str, rcon_port: int, rcon_password: str) -> None:
        sock = socket.socket()
        sock.connect((self.server_ip, self.rcon_port))

        self.server_ip = server_ip
        self.rcon_port = rcon_port
        self.rcon_password = rcon_password

        self.__socket = sock

    async def close_connection(self) -> None:
        self.__socket.close()

    async def send_packet(self, packet_type: int, data: str) -> str:
        packet = struct.pack("<ii", self.SERVER_DATA_RESPONSE_VALUE, packet_type) + \
            data.encode("utf8") + self.EMPTY_BYTE_STRING
        packet_length = struct.pack("<i", len(packet))

        self.__socket.send(packet_length + packet)

        received_message = await self.receive_message()
        return received_message.decode("utf8")

    async def receive_message(self):
        raw_message_length = await self.receive_all_socket_data(4)

        if not raw_message_length:
            return None

        message_length = struct.unpack("<i", raw_message_length)[0]
        return bytes(await self.receive_all_socket_data(message_length))

    async def receive_all_socket_data(self, length):
        data = bytearray()

        while len(data) < length:
            packet = self.__socket.recv(length - len(data))

            if not packet:
                return None

            data.extend(packet)

        return data

    async def execute_command(self, command: str) -> str:
        await self.send_packet(self.SERVER_DATA_AUTH_ID, self.rcon_password)
        command_output = await self.send_packet(self.SERVER_DATA_EXEC_COMMAND_ID, command)

        return command_output
