
from PIL import Image, ImageDraw, ImageFilter
import random, math

def crystal_shape(cx,cy,r,wobble):
    pts=[]
    n=random.randint(5,10)
    for i in range(n):
        ang=2*math.pi*i/n + random.uniform(-0.2,0.2)
        rr=r*(1+random.uniform(-wobble,wobble))
        pts.append((cx+rr*math.cos(ang), cy+rr*math.sin(ang)))
    pts.append(pts[0])
    return pts

def draw_polygon(canvas, pts, color, alpha, blur):
    layer = Image.new("RGBA", canvas.size, (0,0,0,0))
    d = ImageDraw.Draw(layer)
    d.polygon(pts, fill=(*color,int(alpha*255)))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(layer)

def render_crystal(df, palette, layers=8, shapes_per_emotion=20,
                   width=900,height=900):
    base=Image.new("RGBA",(width,height),(10,10,20,255))
    canvas=Image.new("RGBA",(width,height),(0,0,0,0))
    emos = df['emotion'].unique().tolist() if not df.empty else ["joy","calm"]

    for _ in range(layers):
        for e in emos:
            col=palette.get(e,(200,200,200))
            for _ in range(shapes_per_emotion):
                cx,cy=random.randint(50,width-50),random.randint(50,height-50)
                r=random.randint(20,120)
                pts=crystal_shape(cx,cy,r,0.35)
                draw_polygon(canvas, pts, col, 0.5, 4)

    base.alpha_composite(canvas)
    return base.convert("RGB")
