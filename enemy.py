from gameObject import GameObject

class Enemy(GameObject):
    def __init__(self):
        super().__init__()
        self.x_pos = 1350

    # actualiza la posicion en el eje x
    def update(self, speed):
        self.x_pos -= speed

    # corrobora si el objeto mismo ha salido del mapa o de la pantalla
    def is_offscreen(self):
        return self.x_pos + self.obj_width < 0