from PIL import Image, ImageDraw

# Returns an image describing the user's pokedex
# Input:
#   dex_obj:    Array (?) of number_obtained[Pokedex_number - 1]
def user_pokedex(dex_obj):
    images = [Image.open('icons/{}.png'.format(i)) for i in range(1,152)]

    # Fixed width for background; length should be dependent on Pokedex entries
        # Each icon is 30x30, use padding of 2px on all sides, rows of 5
    height_stop = True
    curr = 151
    while(height_stop and curr > -1):
        try:
            if dex_obj[curr] > 0:
                height_stop = False
            else:
                curr -= 1
        except:
            curr -= 1
    bg_w = 2 + (30+2) * 5
    bg_h = 2 + (30+2) * ((curr // 5) + 1)
    background = Image.new('RGBA', (bg_w, bg_h), (255, 255, 255, 255))

    # Print out the first 150 Pokemon (Mew separately)
    x, y = [2, 2]
    for i in range(0, min(len(dex_obj), 150)):
        if dex_obj[i] > 0:
            # Also return number obtained
            draw = ImageDraw.Draw(images[i-1])
            draw.text((1, 20), str(dex_obj[i]), fill=(0,0,0,255))
            # Then paste the image onto the pokedex background
            background.paste(images[i-1], (x, y))
        # when to /r/n
        if i%5 != 4:
            x = x+30+2
        else:
            x = 2
            y = y+30+2

    try:
        if dex_obj[150] > 0:
            x = 2 + (30+2) + (30+2)
            # Also return number obtained
            draw = ImageDraw.Draw(images[150])
            draw.text((1, 20), str(dex_obj[150]), fill=(0,0,0,255))
            background.paste(images[150], (x, y))
    except:
        pass

    background.save('user_dex.png')
