
# coding: utf-8

# In[1]:


from PIL import Image


# In[2]:


ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

# 将256灰度映射到70个字符上
def get_char(r,g,b,alpha = 256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    unit = (256.0 + 1)/length
    return ascii_char[int(gray/unit)]


# In[3]:


img = Image.open("ascii_dora.png")
width,height= img.size
if width > 100 or height > 80:
    img = img.resize((100, 80), Image.NEAREST)
    width = 100
    height = 80
txt = ""
for i in range(height):
        for j in range(width):
            txt += get_char(*img.getpixel((j,i)))
        txt += '\n'

print(txt)

