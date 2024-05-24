from gameObject import GameObject

class Enemy(GameObject):
    def __init__(self):
        super().__init__()
        self.y_pos = 0

    # actualiza la posicion en el eje x
    def update(self, speed):
        self.y_pos += speed

    # corrobora si el objeto mismo ha salido del mapa o de la pantalla
    def is_offscreen(self):
        return self.y_pos + self.obj_width > 600