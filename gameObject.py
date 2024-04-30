class GameObject:
    def __init__(self):
        self.x_pos = 0
        self.y_pos = 0
        self.obj_width = 0
        self.obj_height = 0
        self.image = ""

    # corrobora si el objeto mismo esta chocando con algo (otro objeto)
    def is_collisioning_with(self, anObject):
        return (self.x_pos + self.obj_width > anObject.x_pos and self.x_pos < anObject.x_pos + anObject.obj_width) and (self.y_pos + self.obj_height  > anObject.y_pos and self.y_pos < anObject.y_pos + anObject.obj_height)

    # dibuja la imagen del objeto mismo en la pantalla
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x_pos, self.y_pos))