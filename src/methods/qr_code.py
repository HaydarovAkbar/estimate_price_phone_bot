from qrcode import QRCode, constants


class Generator:
    def __init__(self, data: str, version: int = 2, box_size: int = 8, border: int = 2):
        self.data = data
        self.version = version
        self.box_size = box_size
        self.border = border

    def generate(self):
        qr = QRCode(
            version=self.version,
            error_correction=constants.ERROR_CORRECT_H,
            box_size=self.box_size,
            border=self.border,
        )
        qr.add_data(self.data)
        qr.make(fit=True)
        return qr.make_image(fill_color="black", back_color="white", dark="yellow", light="#323524", scale=5)