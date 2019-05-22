import sys

sys.setrecursionlimit(8000)

def flood_fill(TiledMap, pos, tile_id, tile_obj_light, out_list):
	if(tile_obj_light == 0):
		old_id = TiledMap.map_.grid[pos[0]][pos[1]]
	elif(tile_obj_light == 1):
		old_id = TiledMap.map_.obj_grid[pos[0]][pos[1]]
	else:
		old_id = TiledMap.map_.light_grid[pos[0]][pos[1]]

	if(old_id == tile_id):
		return

	out_list.append(pos)

	if(pos[0]>0 and flood_check(TiledMap, pos, old_id, tile_id, tile_obj_light, out_list, x=-1)):
		sec_flood_fill(TiledMap, [pos[0]-1, pos[1]], old_id, tile_id, tile_obj_light, out_list)
	if(pos[0] < len(TiledMap.map_.grid)-2 and flood_check(TiledMap, pos, old_id, tile_id, tile_obj_light, out_list, x=1)):
		sec_flood_fill(TiledMap, [pos[0]+1, pos[1]], old_id, tile_id, tile_obj_light, out_list)
	if(pos[1]>0 and flood_check(TiledMap, pos, old_id, tile_id, tile_obj_light, out_list, y=-1)):
		sec_flood_fill(TiledMap, [pos[0], pos[1]-1], old_id, tile_id, tile_obj_light, out_list)
	if(pos[1] < len(TiledMap.map_.grid[0])-2 and flood_check(TiledMap, pos, old_id, tile_id, tile_obj_light, out_list, y=1)):
		sec_flood_fill(TiledMap, [pos[0], pos[1]+1], old_id, tile_id, tile_obj_light, out_list)

	return out_list

def sec_flood_fill(TiledMap, pos, ovw_tile, tile_id, tile_obj_light, out_list):

	out_list.append(pos)

	if(pos[0]>0 and flood_check(TiledMap, pos, ovw_tile, tile_id, tile_obj_light, out_list, x=-1)):
		sec_flood_fill(TiledMap, [pos[0]-1, pos[1]], ovw_tile, tile_id, tile_obj_light, out_list)
	if(pos[0] < len(TiledMap.map_.grid)-1 and flood_check(TiledMap, pos, ovw_tile, tile_id, tile_obj_light, out_list, x=1)):
		sec_flood_fill(TiledMap, [pos[0]+1, pos[1]], ovw_tile, tile_id, tile_obj_light, out_list)
	if(pos[1]>0 and flood_check(TiledMap, pos, ovw_tile, tile_id, tile_obj_light, out_list, y=-1)):
		sec_flood_fill(TiledMap, [pos[0], pos[1]-1], ovw_tile, tile_id, tile_obj_light, out_list)
	if(pos[1] < len(TiledMap.map_.grid[0])-1 and flood_check(TiledMap, pos, ovw_tile, tile_id, tile_obj_light, out_list, y=1)):
		sec_flood_fill(TiledMap, [pos[0], pos[1]+1], ovw_tile, tile_id, tile_obj_light, out_list)

def flood_check(TiledMap, pos, ovw_tile, tile_id, tile_obj_light, out_list, x=0, y=0):
	if(tile_obj_light == 0):
		if(TiledMap[pos[0]+x][pos[1]+y] == ovw_tile and [pos[0]+x, pos[1]+y] not in out_list):
			return True
		return False
	elif(tile_obj_light == 1):
		if(TiledMap.map_.obj_grid[pos[0]+x][pos[1]+y] == ovw_tile and [pos[0]+x, pos[1]+y] not in out_list):
			return True
		return False
	elif(tile_obj_light == 2):
		if(TiledMap.map_.light_grid[pos[0]+x][pos[1]+y] == ovw_tile and [pos[0]+x, pos[1]+y] not in out_list):
			return True
		return False

def tupsum(tuple1, tuple2):
	return (tuple1[0]+tuple2[0], tuple1[1]+tuple2[1])