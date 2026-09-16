import pygame
import numpy as np
import moderngl
WALL = 0
MIRROR = 1
light = np.array([450,450], dtype=np.float32)
RAYS = 128 #keep this number as multiples of 64 since we are  using 64 threads per group


pygame.init()
screen = pygame.display.set_mode((900,900), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
ctx = moderngl.create_context()

with open('compute.glsl') as f:
    compute = ctx.compute_shader(f.read())
with open('vert.glsl') as f:
    vert = f.read()
with open('frag.glsl') as f:
    frag = f.read()

display_prog = ctx.program(vertex_shader=vert, fragment_shader=frag)

def build_scene():
    walls = np.array([
        [50,  50,  850,  50,  WALL],
        [850, 50,  850, 850,  WALL],
        [850, 850, 50,  850,  WALL],
        [50,  850, 50,   50,  WALL],
        # A diagonal wall in the middle
        
        # A vertical blocker on the left
        [250, 300, 250, 700, MIRROR],
        
        [400, 700, 700, 700, MIRROR],
    ], dtype=np.float32)
    return walls


def pack_scene(scene):
    data = []
    for seg in scene:
        x1, y1, x2, y2, mat = seg
        y1 = 900 - y1
        y2 = 900 - y2
        data.append(np.float32(x1))
        data.append(np.float32(y1))
        data.append(np.float32(x2))
        data.append(np.float32(y2))
        data.append(np.int32(mat))
        data.append(np.int32(0))
    return np.array(data, dtype=np.float32).tobytes()

MAX_SEGMENTS = 64
ssbo = ctx.buffer(reserve=MAX_SEGMENTS * 24)
scene = build_scene()
ssbo.write(pack_scene(scene))
ssbo.bind_to_storage_buffer(1)

texture = ctx.texture((900,900), 4, dtype='f4')
texture.bind_to_image(0,read=True,write=True)

quad = np.array([-1,-1, 1,-1, -1,1, 1,1], dtype='f4')
quad_vbo = ctx.buffer(quad.tobytes())
quad_vao = ctx.vertex_array(display_prog, [(quad_vbo, '2f', 'in_pos')])

clock = pygame.time.Clock()
dragging_light = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = event.pos
                my = 900 - my
                if abs(mx - light[0]) < 20 and abs(my - light[1]) < 20:
                    dragging_light = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_light = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging_light:
                mx, my = event.pos
                light[0] = mx
                light[1] = my
    texture.write(np.zeros((900,900 , 4), dtype=np.float32).tobytes())

    compute['light_pos'] = (light[0], 900-light[1])
    compute['num_rays'] = RAYS  
    compute['seg_count'] = len(scene)
    compute['width'] = 900.0
    compute['height'] = 900.0
    groups = RAYS// 64
    compute.run(group_x=groups)

    ctx.finish()

    ctx.clear(0, 0, 0)
    texture.use(0)
    display_prog['tex'] = 0
    quad_vao.render(moderngl.TRIANGLE_STRIP)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()