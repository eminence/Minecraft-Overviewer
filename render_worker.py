import traceback
import chunk
from time import sleep

import sys
sys.path.append("./../python-gearman")

from gearman.worker import GearmanWorker

w = GearmanWorker(['192.168.1.4'])

import cPickle
import textures
from PIL import Image, ImageDraw, ImageEnhance
import zlib

def renderer(worker, job):
    try:
        print "got a job"
        raw_data = zlib.decompress(job.data)
        important = cPickle.loads(raw_data)
        print "  ", important.keys()

        cave = important['cave']
        blockData_expanded = important['blockData_expanded']
        blocks = important['blocks']
        transparent_blocks = chunk.transparent_blocks
        xoff = important['xoff']
        yoff = important['yoff']

        depth_colors = chunk.depth_colors
        tileEntities = important['tileEntities']

        img = Image.new("RGBA", (384, 1728), (38,92,255,0))
        
        for x,y,z,imgx,imgy in chunk.iterate_chunkblocks(xoff,yoff):
            blockid = blocks[x,y,z]
            if blockid in textures.special_blocks:
                ancilData = blockData_expanded[x,y,z]
                try:
                    t = textures.specialblockmap[(blockid, ancilData)]
                except KeyError:
                    t = None

            else:
                t = textures.blockmap[blockid]
                
            if not t:
                continue


            # Check if this block is occluded
            if cave and (
                    x == 0 and y != 15 and z != 127
            ):
                # If it's on the x face, only render if there's a
                # transparent block in the y+1 direction OR the z-1
                # direction
                if (
                    blocks[x,y+1,z] not in transparent_blocks and
                    blocks[x,y,z+1] not in transparent_blocks
                ):
                    continue
            elif cave and (
                    y == 15 and x != 0 and z != 127
            ):
                # If it's on the facing y face, only render if there's
                # a transparent block in the x-1 direction OR the z-1
                # direction
                if (
                    blocks[x-1,y,z] not in transparent_blocks and
                    blocks[x,y,z+1] not in transparent_blocks
                ):
                    continue
            elif cave and (
                    y == 15 and x == 0 and z != 127
            ):
                # If it's on the facing edge, only render if what's
                # above it is transparent
                if (
                    blocks[x,y,z+1] not in transparent_blocks
                ):
                    continue
            elif (
                    # Normal block or not cave mode, check sides for
                    # transparentcy or render unconditionally if it's
                    # on a shown face
                    x != 0 and y != 15 and z != 127 and
                    blocks[x-1,y,z] not in transparent_blocks and
                    blocks[x,y+1,z] not in transparent_blocks and
                    blocks[x,y,z+1] not in transparent_blocks
            ):
                # Don't render if all sides aren't transparent and
                # we're not on the edge
                continue



            # Draw the actual block on the image. For cave images,
            # tint the block with a color proportional to its depth
            if cave:
                # no lighting for cave -- depth is probably more useful
                img.paste(Image.blend(t[0],depth_colors[z],0.3), (imgx, imgy), t[1])
            else:
                # no lighting at all
                img.paste(t[0], (imgx, imgy), t[1])

            # Draw edge lines
            if blockid in (44,): # step block
               increment = 6
            elif blockid in (78,): # snow
               increment = 9
            else:
               increment = 0

            if blockid not in transparent_blocks or blockid in (78,): #special case snow so the outline is still drawn
                draw = ImageDraw.Draw(img)
                if x != 15 and blocks[x+1,y,z] == 0:
                    draw.line(((imgx+12,imgy+increment), (imgx+22,imgy+5+increment)), fill=(0,0,0), width=1)
                if y != 0 and blocks[x,y-1,z] == 0:
                    draw.line(((imgx,imgy+6+increment), (imgx+12,imgy+increment)), fill=(0,0,0), width=1)


        for entity in tileEntities:
            if entity['id'] == 'Sign':

                # convert the blockID coordinates from local chunk
                # coordinates to global world coordinates
                newPOI = dict(type="sign",
                                x= entity['x'],
                                y= entity['z'],
                                z= entity['y'],
                                msg="%s\n%s\n%s\n%s" %
                                   (entity['Text1'], entity['Text2'], entity['Text3'], entity['Text4']),
                                chunk= (self.chunkX, self.chunkY),
                               )
                #self.queue.put(["newpoi", newPOI])


        # check to see if there are any signs in the persistentData list that are from this chunk.
        # if so, remove them from the persistentData list (since they're have been added to the world.POI
        # list above.
        #self.queue.put(['removePOI', (self.chunkX, self.chunkY)])

            

        #return img
        return zlib.compress(img.tostring())
    except:
        print "caught an exception!"
        traceback.print_exc()


w.register_task('go_render', renderer)
print "ready to go!"

w.work()
